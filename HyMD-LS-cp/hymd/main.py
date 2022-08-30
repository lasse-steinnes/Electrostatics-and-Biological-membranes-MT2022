"""Main simulation driver module
"""
import datetime
import h5py
import logging
from mpi4py import MPI
import numpy as np
import pmesh.pm as pmesh
import warnings
from .configure_runtime import configure_runtime
from .hamiltonian import DefaultNoChi, DefaultWithChi, SquaredPhi
from .input_parser import check_config, sort_dielectric_by_type_id, get_charges_types_list
from .logger import Logger, format_timedelta
from .file_io import distribute_input, OutDataset, store_static, store_data
from .field import (compute_field_force, update_field,
                    compute_field_and_kinetic_energy, domain_decomposition,
                    update_field_force_q, compute_field_energy_q,
                    update_field_force_q_GPE, compute_field_energy_q_GPE,
                    initialize_pm)
from .thermostat import (csvr_thermostat, cancel_com_momentum,
                         generate_initial_velocities)
from .force import dipole_forces_redistribution, prepare_bonds
from .integrator import integrate_velocity, integrate_position
from .pressure import comp_pressure
from .barostat import isotropic, semiisotropic


def main():
    """Main simulation driver

    Initializes structure, topology, and simulation configuration and iterates
    the molecular dynamics loop.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        start_time = datetime.datetime.now()

    args, config = configure_runtime(comm)

    if args.double_precision:
        dtype = np.float64
        from .force import (
            compute_bond_forces__fortran__double as compute_bond_forces
        )
        from .force import (
            compute_angle_forces__fortran__double as compute_angle_forces
        )
        from .force import (
            compute_dihedral_forces__fortran__double as compute_dihedral_forces
        )
    else:
        dtype = np.float32
        from .force import (
            compute_bond_forces__fortran as compute_bond_forces
        )
        from .force import (
            compute_angle_forces__fortran as compute_angle_forces
        )
        from .force import (
            compute_dihedral_forces__fortran as compute_dihedral_forces
        )

    driver = "mpio" if not args.disable_mpio else None
    _kwargs = {"driver": driver, "comm": comm} if not args.disable_mpio else {}
    with h5py.File(args.input, "r", **_kwargs) as in_file:
        rank_range, molecules_flag = distribute_input(
            in_file,
            rank,
            size,
            config.n_particles,
            config.max_molecule_size if config.max_molecule_size else 201,
            comm=comm,
        )
        indices = in_file["indices"][rank_range]
        positions = in_file["coordinates"][-1, rank_range, :]
        positions = positions.astype(dtype)
        if "velocities" in in_file:
            velocities = in_file["velocities"][-1, rank_range, :]
            velocities = velocities.astype(dtype)
        else:
            velocities = np.zeros_like(positions, dtype=dtype)

        names = in_file["names"][rank_range]

        types = None
        bonds = None
        molecules = []
        if "types" in in_file:
            types = in_file["types"][rank_range]
        if molecules_flag:
            molecules = in_file["molecules"][rank_range]
            bonds = in_file["bonds"][rank_range]
        if "charge" in in_file:
            charges = in_file["charge"][rank_range]
            charges_flag = True
        else:
            charges_flag = False

        if "box" in in_file:
            input_box = in_file["box"][:]
        else:
            input_box = np.array( [None, None, None] )

    config = check_config(config, indices, names, types, input_box, comm=comm)

    ## dielectric from toml
    if config.coulombtype == 'PIC_Spectral_GPE':
        config_charges = get_charges_types_list(config, types, charges, comm = comm)
        dielectric_sorted = sort_dielectric_by_type_id(config,charges,types)
        dielectric_flag = True

        if config.convergence_type is not None:
            if config.convergence_type == 'csum':
                def conv_fun(comm,diff_mesh):
                    return diff_mesh.csum() # check if allreduce needed

            elif config.convergence_type == 'euclidean_norm':
                def conv_fun(comm,diff_mesh):
                    return diff_mesh.cnorm() # check if allreduce nedded

            elif config.convergence_type == 'max_diff':
                def conv_fun(comm,diffmesh):
                    msg = np.max(diffmesh)
                    res = comm.allreduce(sendobj=msg, op=MPI.MAX)
                    return res

        else: ## default choice is the max difference if not specified
            config.convergence_type = 'max_diff'
            def conv_fun(comm,diffmesh):
                msg = np.max(diffmesh)
                res = comm.allreduce(sendobj=msg, op=MPI.MAX)
                return res

    else:
        dielectric_flag = False

    if config.n_print:
        if config.n_flush is None:
            config.n_flush = 10000 // config.n_print

    if config.start_temperature:
        velocities = generate_initial_velocities(velocities, config, comm=comm)
    elif config.cancel_com_momentum:
        velocities = cancel_com_momentum(velocities, config, comm=comm)

    bond_forces = np.zeros_like(positions)
    angle_forces = np.zeros_like(positions)
    dihedral_forces = np.zeros_like(positions)
    reconstructed_forces = np.zeros_like(positions)
    field_forces = np.zeros_like(positions)
    elec_forces = np.zeros_like(positions)

    positions = np.mod(positions, config.box_size[None, :])

    # Initialize dipoles, populate them if protein_flag == True
    if args.disable_dipole:
        dipole_flag = 0
    else:
        dipole_flag = 1
    protein_flag = 0
    dipole_positions = np.zeros(shape=(4, 3), dtype=dtype)
    dipole_forces = np.zeros(shape=(4, 3))
    dipole_charges = np.zeros(shape=4)
    transfer_matrices = np.zeros(shape=(6, 3, 3), dtype=dtype)

    # Initialize energies
    field_energy = 0.0
    bond_energy = 0.0
    angle_energy = 0.0
    dihedral_energy = 0.0
    kinetic_energy = 0.0
    field_q_energy = 0.0

    if config.hamiltonian.lower() == "defaultnochi":
        hamiltonian = DefaultNoChi(config)
    elif config.hamiltonian.lower() == "defaultwithchi":
        hamiltonian = DefaultWithChi(
            config, config.unique_names, config.type_to_name_map
        )
    elif config.hamiltonian.lower() == "squaredphi":
        hamiltonian = SquaredPhi(config)
    else:
        err_str = (
            f"The specified Hamiltonian {config.hamiltonian} was not "
            f"recognized as a valid Hamiltonian."
        )
        Logger.rank0.log(logging.ERROR, err_str)
        if rank == 0:
            raise NotImplementedError(err_str)

    pm_stuff  = initialize_pm(pmesh, config, comm)
    (pm, field_list, coulomb_list,elec_list_common) = pm_stuff
    [phi, phi_fourier, force_on_grid, v_ext_fourier, v_ext, phi_transfer,
            phi_gradient, phi_laplacian, phi_lap_filtered_fourier, phi_lap_filtered,
            phi_grad_lap_fourier, phi_grad_lap, v_ext1
            ] = field_list

    if len(elec_list_common) == 3:
        [phi_q, phi_q_fourier, elec_field] = elec_list_common

    if len(coulomb_list)==6:
        [phi_q, phi_q_fourier, elec_field_fourier, elec_field, elec_energy_field,
        Vbar_elec
                ] = coulomb_list

    elif len(coulomb_list)==13:
            [
                phi_eps, phi_eps_fourier,
                phi_eta, phi_eta_fourier, phi_pol,
                phi_pol_prev, elec_dot, elec_field_contrib, elec_potential, Vbar_elec, Vbar_elec_fourier,
                force_mesh_elec, force_mesh_elec_fourier
                ] = coulomb_list

    Logger.rank0.log(logging.INFO, f"pfft-python processor mesh: {str(pm.np)}")

    args_in = [
        velocities,
        indices,
        bond_forces,
        angle_forces,
        dihedral_forces,
        reconstructed_forces,
        field_forces,
        names,
        types,
    ]
    args_recv = [
        "positions",
        "velocities",
        "indices",
        "bond_forces",
        "angle_forces",
        "dihedral_forces",
        "reconstructed_forces",
        "field_forces",
        "names",
        "types",
    ]

    if charges_flag:
        args_in.append(charges)
        args_in.append(elec_forces)
        args_recv.append("charges")
        args_recv.append("elec_forces")

    if dielectric_flag:
        args_in.append(dielectric_sorted)
        args_recv.append('dielectric_sorted')

    if molecules_flag:
        args_recv.append("bonds")
        args_recv.append("molecules")

    _str_receive_dd = ",".join(args_recv)
    _cmd_receive_dd = f"({_str_receive_dd}) = dd"

    if config.domain_decomposition:
        dd = domain_decomposition(
            positions,
            pm,
            *tuple(args_in),
            molecules=molecules if molecules_flag else None,
            bonds=bonds if molecules_flag else None,
            verbose=args.verbose,
            comm=comm,
        )

        exec(_cmd_receive_dd)

    if not args.disable_field:
        layouts = [pm.decompose(positions[types == t]) for t in range(config.n_types)]  # noqa: E501
        update_field(
            phi,
            phi_gradient,
            phi_laplacian,
            phi_transfer,
            phi_grad_lap_fourier,
            phi_grad_lap,
            layouts,
            force_on_grid,
            hamiltonian,
            pm,
            positions,
            types,
            config,
            v_ext,
            phi_fourier,
            phi_lap_filtered_fourier,
            v_ext_fourier,
            phi_lap_filtered,
            v_ext1,
            config.m,
            compute_potential=True,
        ) ## Old input: phi, layouts, force_on_grid, hamiltonian, pm, positions, types,   ##config, v_ext, phi_fourier, v_ext_fourier, compute_potential=True,


        field_energy, kinetic_energy = compute_field_and_kinetic_energy(
            phi,
            phi_gradient,
            velocities,
            hamiltonian,
            positions,
            types,
            v_ext,
            config,
            layouts,
            comm=comm,
        ) ##   old input  phi, velocities, hamiltonian, positions, types, v_ext, config,    layouts, comm=comm,

        compute_field_force(
            layouts, positions, force_on_grid, field_forces, types,
            config.n_types
        )
    else:
        kinetic_energy = comm.allreduce(
            0.5 * config.mass * np.sum(velocities**2)
        )

    if charges_flag:
        layout_q = pm.decompose(positions)
        if config.coulombtype == 'PIC_Spectral_GPE': #dielectric_flag
            Vbar_elec, phi_eps, elec_dot = update_field_force_q_GPE(
                conv_fun, phi, types, charges, config_charges,
                phi_q, phi_q_fourier, phi_eps, phi_eps_fourier,
                phi_eta,
                phi_eta_fourier, phi_pol_prev, phi_pol,
                elec_field, elec_forces, elec_field_contrib, elec_potential,
                Vbar_elec, Vbar_elec_fourier, force_mesh_elec, force_mesh_elec_fourier,
                hamiltonian, layout_q, layouts, pm, positions, config, comm = comm,
                )



            field_q_energy = compute_field_energy_q_GPE(
                config, phi_eps,field_q_energy,
                elec_dot,
                comm=comm
                )


        if config.coulombtype == "PIC_Spectral":
            update_field_force_q(
                charges, phi_q, phi_q_fourier, elec_field_fourier, elec_field,
                elec_forces, layout_q, pm, positions, config,
            )

            field_q_energy = compute_field_energy_q(
                config, phi_q_fourier, elec_energy_field, field_q_energy,
                comm=comm,
            )

    if molecules_flag:
        if not (args.disable_bonds
                and args.disable_angle_bonds
                and args.disable_dihedrals):

            bonds_prep = prepare_bonds(
                molecules, names, bonds, indices, config
            )
            (
                # two-particle bonds
                bonds_2_atom1, bonds_2_atom2, bonds_2_equilibrium,
                bonds_2_stength,
                # three-particle bonds
                bonds_3_atom1, bonds_3_atom2, bonds_3_atom3,
                bonds_3_equilibrium, bonds_3_stength,
                # four-particle bonds
                bonds_4_atom1, bonds_4_atom2, bonds_4_atom3, bonds_4_atom4,
                bonds_4_coeff, bonds_4_type, bonds_4_last,
            ) = bonds_prep

            bonds_4_coeff = np.asfortranarray(bonds_4_coeff)

            if bonds_4_type.any() > 1:
                err_str = (
                    "0 and 1 are the only currently supported dihedral angle "
                    "types."
                )
                Logger.rank0.log(logging.ERROR, err_str)
                if rank == 0:
                    raise NotImplementedError(err_str)

            # Check if we have a protein
            protein_flag = comm.allreduce(bonds_4_type.any() == 1)
            if protein_flag and not args.disable_dipole:
                # Each rank will have different n_tors, we do not need to
                # domain decompose dipoles
                n_tors = len(bonds_4_atom1)
                dipole_positions = np.zeros((n_tors, 4, 3), dtype=dtype)
                # 4 because we need to take into account the last angle in the
                # molecule
                dipole_charges = np.array(
                    [
                        2 * [0.25, -0.25]
                        if (bonds_4_type[i], bonds_4_last[i]) == (1, 1)
                        else [0.25, -0.25, 0.0, 0.0]
                        if bonds_4_type[i] == 1
                        else 2 * [0.0, 0.0]
                        for i in range(n_tors)
                    ],
                    dtype=dtype,
                ).flatten()
                dipole_forces = np.zeros_like(dipole_positions)
                transfer_matrices = np.zeros(
                    shape=(n_tors, 6, 3, 3), dtype=dtype
                )
                phi_dipoles = pm.create("real", value=0.0)
                phi_dipoles_fourier = pm.create("complex", value=0.0)
                dipoles_field_fourier = [
                    pm.create("complex", value=0.0) for _ in range(_SPACE_DIM)
                ]
                dipoles_field = [
                    pm.create("real", value=0.0) for _ in range(_SPACE_DIM)
                ]

        positions = np.asfortranarray(positions)
        velocities = np.asfortranarray(velocities)
        bond_forces = np.asfortranarray(bond_forces)
        angle_forces = np.asfortranarray(angle_forces)
        dihedral_forces = np.asfortranarray(dihedral_forces)
        dipole_positions = np.asfortranarray(dipole_positions)
        transfer_matrices = np.asfortranarray(transfer_matrices)

        if not args.disable_bonds:
            bond_energy_, bond_pr_ = compute_bond_forces(
                bond_forces, positions, config.box_size, bonds_2_atom1,
                bonds_2_atom2, bonds_2_equilibrium, bonds_2_stength,
            )
            bond_energy = comm.allreduce(bond_energy_, MPI.SUM)
        else:
            bonds_2_atom1, bonds_2_atom2 = [], []
        if not args.disable_angle_bonds:
            angle_energy_, angle_pr_ = compute_angle_forces(
                angle_forces, positions, config.box_size, bonds_3_atom1,
                bonds_3_atom2, bonds_3_atom3, bonds_3_equilibrium,
                bonds_3_stength,
            )
            angle_energy = comm.allreduce(angle_energy_, MPI.SUM)
            #angle_pr = comm.allreduce(angle_pr_, MPI.SUM)

        if not args.disable_dihedrals:
            dihedral_energy_ = compute_dihedral_forces(
                dihedral_forces, positions, dipole_positions,
                transfer_matrices, config.box_size, bonds_4_atom1,
                bonds_4_atom2, bonds_4_atom3, bonds_4_atom4, bonds_4_coeff,
                bonds_4_type, bonds_4_last, dipole_flag,
            )
            dihedral_energy = comm.allreduce(dihedral_energy_, MPI.SUM)

        if protein_flag and not args.disable_dipole:
            dipole_positions = np.reshape(dipole_positions, (4 * n_tors, 3))
            dipole_forces = np.reshape(dipole_forces, (4 * n_tors, 3))

            layout_dipoles = pm.decompose(dipole_positions)
            update_field_force_q(
                dipole_charges, phi_dipoles, phi_dipoles_fourier,
                dipoles_field_fourier, dipoles_field, dipole_forces,
                layout_dipoles, pm, dipole_positions, config,
            )

            dipole_positions = np.reshape(dipole_positions, (n_tors, 4, 3))
            dipole_forces = np.reshape(dipole_forces, (n_tors, 4, 3))

            dipole_positions = np.asfortranarray(dipole_positions)
            dipole_forces_redistribution(
                reconstructed_forces, dipole_forces, transfer_matrices,
                bonds_4_atom1, bonds_4_atom2, bonds_4_atom3, bonds_4_atom4,
                bonds_4_type, bonds_4_last,
            )

    else:
        #bonds_2_atom1, bonds_2_atom2 = None, None
        bonds_2_atom1, bonds_2_atom2 = [], []

    config.initial_energy = (
        field_energy + kinetic_energy + bond_energy + angle_energy
        + dihedral_energy + field_q_energy
    )

    out_dataset = OutDataset(
        args.destdir, config, double_out=args.double_output,
        disable_mpio=args.disable_mpio,
    )

    store_static(
        out_dataset, rank_range, names, types, indices, config, bonds_2_atom1,
        bonds_2_atom2, molecules=molecules if molecules_flag else None,
        velocity_out=args.velocity_output, force_out=args.force_output,
        charges= charges if charges_flag else False,
        dielectrics = dielectric_sorted if dielectric_flag else False,
        comm=comm,
    )

    if config.n_print > 0:
        step = 0
        frame = 0
        if not args.disable_field:
            field_energy, kinetic_energy = compute_field_and_kinetic_energy(
                phi, phi_gradient, velocities, hamiltonian, positions, types, v_ext, config,
                layouts, comm=comm,
            )
        else:
            kinetic_energy = comm.allreduce(
                0.5 * config.mass * np.sum(velocities ** 2)
            )


        temperature = (
            (2 / 3) * kinetic_energy / (config.gas_constant * config.n_particles)  # noqa: E501
        )

        if config.pressure or config.barostat:
            pressure = comp_pressure(
                    phi,
                    phi_gradient,
                    hamiltonian,
                    velocities,
                    config,
                    phi_fourier,
                    phi_laplacian,
                    phi_transfer,
                    phi_grad_lap_fourier,
                    phi_grad_lap,
                    args,
                    bond_forces,
                    angle_forces,
                    positions,
                    bond_pr_,
                    angle_pr_,
                    Vbar_elec,
                    comm=comm
            )

            #if rank ==0 : print(pressure[9:12])
            #print('phi_fft after pressure call: phi_fft[d=0]',phi_fft[0].value[0][0][0:2])
        else:
            pressure = 0.0 #0.0 indicates not calculated. To be changed.

        forces_out = (
            field_forces + bond_forces + angle_forces + dihedral_forces
            + reconstructed_forces
        )


        store_data(
            out_dataset, step, frame, indices, positions, velocities,
            forces_out, config.box_size, temperature, pressure, kinetic_energy,
            bond_energy, angle_energy, dihedral_energy, field_energy,
            field_q_energy, config.time_step, config,
            velocity_out=args.velocity_output, force_out=args.force_output,
            charge_out=charges_flag, dump_per_particle=args.dump_per_particle,
            comm=comm,
        )

    if rank == 0:
        loop_start_time = datetime.datetime.now()
        last_step_time = datetime.datetime.now()

    # MD loop
    for step in range(config.n_steps):
        current_step_time = datetime.datetime.now()

        if step == 0 and args.verbose > 1:
            Logger.rank0.log(logging.INFO, f"MD step = {step:10d}")
        else:
            log_step = False
            if config.n_steps < 1000:
                log_step = True
            elif (
                np.mod(step, config.n_steps // 1000) == 0
                or np.mod(step, config.n_print) == 0
            ):
                log_step = True
            if rank == 0 and log_step and args.verbose > 1:
                step_t = current_step_time - last_step_time
                tot_t = current_step_time - loop_start_time
                ns_sim = (
                    (step + 1) * config.respa_inner * config.time_step / 1000.0
                )

                seconds_per_day = 24 * 60 * 60
                seconds_elapsed = tot_t.days * seconds_per_day
                seconds_elapsed += tot_t.seconds
                seconds_elapsed += 1e-6 * tot_t.microseconds
                minutes_elapsed = seconds_elapsed / 60
                hours_elapsed = minutes_elapsed / 60
                days_elapsed = hours_elapsed / 24

                ns_per_day = ns_sim / days_elapsed
                hours_per_ns = hours_elapsed / ns_sim
                steps_per_s = (step + 1) / seconds_elapsed
                info_str = (
                    f"MD step = {step:10d}   step time: "
                    f"{format_timedelta(step_t):22s}   Performance: "
                    f"{ns_per_day:.3f} ns/day   {hours_per_ns:.3f} hours/ns   "
                    f"{steps_per_s:.3f} steps/s"
                )
                Logger.rank0.log(logging.INFO, info_str)

        # Initial outer rRESPA velocity step
        velocities = integrate_velocity(
            velocities, field_forces / config.mass,
            config.respa_inner * config.time_step,
        )

        if charges_flag and (config.coulombtype == "PIC_Spectral" \
                    or config.coulombtype == "PIC_Spectral_GPE"):
            velocities = integrate_velocity(
                velocities, elec_forces / config.mass,
                config.respa_inner * config.time_step,
            )

        if protein_flag:
            velocities = integrate_velocity(
                velocities, reconstructed_forces / config.mass,
                config.respa_inner * config.time_step,
            )

        # Inner rRESPA steps
        for inner in range(config.respa_inner):
            velocities = integrate_velocity(
                velocities,
                (bond_forces + angle_forces + dihedral_forces) / config.mass,
                config.time_step,
            )
            positions = integrate_position(
                positions, velocities, config.time_step
            )
            positions = np.mod(positions, config.box_size[None, :])

            # Update fast forces
            if molecules_flag:
                if not args.disable_bonds:
                    bond_energy, bond_pr_ = compute_bond_forces(
                        bond_forces, positions, config.box_size, bonds_2_atom1,
                        bonds_2_atom2, bonds_2_equilibrium, bonds_2_stength,
                    )
                if not args.disable_angle_bonds:
                    angle_energy_, angle_pr_  = compute_angle_forces(
                        angle_forces, positions, config.box_size,
                        bonds_3_atom1, bonds_3_atom2, bonds_3_atom3,
                        bonds_3_equilibrium, bonds_3_stength,
                    )
                if not args.disable_dihedrals:
                    if (
                        inner == config.respa_inner - 1
                        and not args.disable_dipole
                    ):
                        dipole_flag = 1
                    else:
                        dipole_flag = 0
                    dihedral_energy_ = compute_dihedral_forces(
                        dihedral_forces, positions, dipole_positions,
                        transfer_matrices, config.box_size, bonds_4_atom1,
                        bonds_4_atom2, bonds_4_atom3, bonds_4_atom4,
                        bonds_4_coeff, bonds_4_type, bonds_4_last, dipole_flag,
                    )

            velocities = integrate_velocity(
                velocities,
                (bond_forces + angle_forces + dihedral_forces) / config.mass,
                config.time_step,
            )

        # Berendsen Barostat
        if config.barostat:
            if config.barostat.lower() == 'isotropic':
                pm_stuff, change = isotropic(
                     pmesh,
                     pm_stuff,
                     phi,
                     phi_gradient,
                     hamiltonian,
                     positions,
                     velocities,
                     config,
                     phi_fourier,
                     phi_laplacian,
                     phi_transfer,
                     phi_grad_lap_fourier,
                     phi_grad_lap,
                     bond_forces,
                     angle_forces,
                     args,
                     bond_pr_,
                     angle_pr_,
                     Vbar_elec,
                     step,
                     comm=comm
                )

            elif config.barostat.lower() == 'semiisotropic':
                pm_stuff, change = semiisotropic(
                     pmesh,
                     pm_stuff,
                     phi,
                     phi_gradient,
                     hamiltonian,
                     positions,
                     velocities,
                     config,
                     phi_fourier,
                     phi_laplacian,
                     phi_transfer,
                     phi_grad_lap_fourier,
                     phi_grad_lap,
                     bond_forces,
                     angle_forces,
                     args,
                     bond_pr_,
                     angle_pr_,
                     Vbar_elec,
                     step,
                     comm=comm
                )
            (pm, field_list, coulomb_list,elec_list_common) = pm_stuff
            [phi, phi_fourier, force_on_grid, v_ext_fourier, v_ext, phi_transfer,
                    phi_gradient, phi_laplacian, phi_lap_filtered_fourier, phi_lap_filtered,
                    phi_grad_lap_fourier, phi_grad_lap, v_ext1
                    ] = field_list

            if len(elec_list_common) == 3:
                [phi_q, phi_q_fourier, elec_field] = elec_list_common

            if len(coulomb_list) == 6:
                [phi_q, phi_q_fourier, elec_field_fourier, elec_field, elec_energy_field,
                Vbar_elec
                        ] = coulomb_list

            elif len(coulomb_list) == 13:
                [
                        phi_eps, phi_eps_fourier,
                        phi_eta, phi_eta_fourier, phi_pol,
                        phi_pol_prev, elec_dot, elec_field_contrib, elec_potential, Vbar_elec, Vbar_elec_fourier,
                        force_mesh_elec, force_mesh_elec_fourier
                        ] = coulomb_list

        # Update slow forces
        if not args.disable_field:
            #print("update phi w rank", comm.Get_rank())
            layouts = [
                pm.decompose(positions[types == t]) for t in range(config.n_types)  # noqa: E501
            ]
            update_field(
                phi,phi_gradient, phi_laplacian, phi_transfer,phi_grad_lap_fourier, phi_grad_lap, layouts,
                force_on_grid, hamiltonian, pm, positions, types,
                config, v_ext, phi_fourier, phi_lap_filtered_fourier, v_ext_fourier, phi_lap_filtered,
                v_ext1, config.m,
            )
            compute_field_force(
                layouts, positions, force_on_grid, field_forces, types,
                config.n_types,
            )

            if charges_flag:
                layout_q = pm.decompose(positions)
                #print(charges)
                #print(config.name_to_type_map)
                if config.coulombtype == "PIC_Spectral_GPE": # dielectric_flag and
                    Vbar_elec, phi_eps, elec_dot = update_field_force_q_GPE(
                        conv_fun, phi, types, charges, config_charges,
                        phi_q, phi_q_fourier, phi_eps, phi_eps_fourier,
                        phi_eta,
                        phi_eta_fourier, phi_pol_prev, phi_pol,
                        elec_field, elec_forces, elec_field_contrib, elec_potential,
                        Vbar_elec, Vbar_elec_fourier, force_mesh_elec, force_mesh_elec_fourier,
                        hamiltonian, layout_q, layouts, pm, positions, config, comm = comm,
                        )


                    field_q_energy =compute_field_energy_q_GPE(
                        config, phi_eps,
                        field_q_energy,elec_dot,
                        comm=comm
                    )

                if config.coulombtype == "PIC_Spectral":
                    update_field_force_q(
                        charges, phi_q, phi_q_fourier, elec_field_fourier,
                        elec_field, elec_forces, layout_q, pm, positions, config,
                    )
                    field_q_energy = compute_field_energy_q(
                        config, phi_q_fourier, elec_energy_field, field_q_energy,
                        comm=comm,
                    )


            if protein_flag and not args.disable_dipole:
                dipole_positions = np.reshape(
                    dipole_positions, (4 * n_tors, 3)
                )
                dipole_forces = np.reshape(
                    dipole_forces, (4 * n_tors, 3)
                )

                layout_dipoles = pm.decompose(dipole_positions)
                update_field_force_q(
                    dipole_charges, phi_dipoles, phi_dipoles_fourier,
                    dipoles_field_fourier, dipoles_field, dipole_forces,
                    layout_dipoles, pm, dipole_positions, config,
                )

                dipole_positions = np.reshape(dipole_positions, (n_tors, 4, 3))
                dipole_forces = np.reshape(dipole_forces, (n_tors, 4, 3))

                dipole_positions = np.asfortranarray(dipole_positions)
                dipole_forces_redistribution(
                    reconstructed_forces, dipole_forces, transfer_matrices,
                    bonds_4_atom1, bonds_4_atom2, bonds_4_atom3, bonds_4_atom4,
                    bonds_4_type, bonds_4_last,
                )

        # Second rRESPA velocity step
        velocities = integrate_velocity(
            velocities, field_forces / config.mass,
            config.respa_inner * config.time_step,
        )

        if charges_flag and (config.coulombtype == "PIC_Spectral" or config.coulombtype == "PIC_Spectral_GPE"):
            velocities = integrate_velocity(
                velocities, elec_forces / config.mass,
                config.respa_inner * config.time_step,
            )
        if protein_flag and not args.disable_dipole:
            velocities = integrate_velocity(
                velocities, reconstructed_forces / config.mass,
                config.respa_inner * config.time_step,
            )

        # Only compute and keep the molecular bond energy from the last rRESPA
        # inner step
        if molecules_flag:
            if not args.disable_bonds:
                bond_energy = comm.allreduce(bond_energy_, MPI.SUM)
            if not args.disable_angle_bonds:
                angle_energy = comm.allreduce(angle_energy_, MPI.SUM)
            if not args.disable_dihedrals:
                dihedral_energy = comm.allreduce(dihedral_energy_, MPI.SUM)

        if step != 0 and config.domain_decomposition:
            if np.mod(step, config.domain_decomposition) == 0:
                positions = np.ascontiguousarray(positions)
                bond_forces = np.ascontiguousarray(bond_forces)
                angle_forces = np.ascontiguousarray(angle_forces)
                dihedral_forces = np.ascontiguousarray(dihedral_forces)

                args_in = [
                    velocities, indices, bond_forces, angle_forces,
                    dihedral_forces, reconstructed_forces, field_forces, names,
                    types,
                ]

                if charges_flag:
                    args_in.append(charges)
                    args_in.append(elec_forces)

                if dielectric_flag: ## add dielectric related
                    args_in.append(dielectric_sorted)

                dd = domain_decomposition(  # noqa: F841
                    positions, pm, *tuple(args_in),
                    molecules=molecules if molecules_flag else None,
                    bonds=bonds if molecules_flag else None,
                    verbose=args.verbose, comm=comm,
                )
                exec(_cmd_receive_dd)

                positions = np.asfortranarray(positions)
                bond_forces = np.asfortranarray(bond_forces)
                angle_forces = np.asfortranarray(angle_forces)
                dihedral_forces = np.asfortranarray(dihedral_forces)

                layouts = [
                    pm.decompose(positions[types == t]) for t in range(config.n_types)  # noqa: E501
                ]
                if molecules_flag:
                    bonds_prep = prepare_bonds(
                        molecules, names, bonds, indices, config
                    )
                    (
                        # two-particle bonds
                        bonds_2_atom1, bonds_2_atom2, bonds_2_equilibrium,
                        bonds_2_stength,
                        # three-particle bonds
                        bonds_3_atom1, bonds_3_atom2, bonds_3_atom3,
                        bonds_3_equilibrium, bonds_3_stength,
                        # four-particle bonds
                        bonds_4_atom1, bonds_4_atom2, bonds_4_atom3,
                        bonds_4_atom4, bonds_4_coeff, bonds_4_type,
                        bonds_4_last,
                    ) = bonds_prep

                    bonds_4_coeff = np.asfortranarray(bonds_4_coeff)

                    # Reinitialize dipoles so each rank has the right amount
                    if protein_flag and not args.disable_dipole:
                        # Each rank will have different n_tors, we don't need
                        # to domain decompose dipoles
                        n_tors = len(bonds_4_atom1)
                        dipole_positions = np.zeros(
                            (n_tors, 4, 3), dtype=dtype
                        )

                        # 4 because we need to take into account the last angle
                        # in the molecule
                        dipole_charges = np.array(
                            [
                                2 * [0.25, -0.25]
                                if (bonds_4_type[i], bonds_4_last[i]) == (1, 1)
                                else [0.25, -0.25, 0.0, 0.0]
                                if bonds_4_type[i] == 1
                                else 2 * [0.0, 0.0]
                                for i in range(n_tors)
                            ],
                            dtype=dtype,
                        ).flatten()
                        dipole_forces = np.zeros_like(dipole_positions)
                        transfer_matrices = np.zeros(
                            shape=(n_tors, 6, 3, 3), dtype=dtype
                        )
                        dipole_positions = np.asfortranarray(dipole_positions)
                        transfer_matrices = np.asfortranarray(transfer_matrices)  # noqa: E501

        for t in range(config.n_types):
            if args.verbose > 2:
                exchange_cost = layouts[t].get_exchange_cost()
                Logger.all_ranks.log(
                    logging.INFO,
                    (
                        f"(GHOSTS: Total number of particles of type "
                        f"{config.type_to_name_map[t]} to be "
                        f"exchanged = {exchange_cost[rank]}"
                    ),
                )

        # Thermostat
        if config.target_temperature and np.mod(step, config.n_b)==0:
            csvr_thermostat(velocities, names, config, comm=comm)

        # Remove total linear momentum
        if config.cancel_com_momentum:
            if np.mod(step, config.cancel_com_momentum) == 0:
                velocities = cancel_com_momentum(velocities, config, comm=comm)

        # Print trajectory
        if config.n_print > 0:
            if np.mod(step, config.n_print) == 0 and step != 0:
                frame = step // config.n_print
                if not args.disable_field:
                    layouts = [pm.decompose(positions[types == t]) for t in range(config.n_types)]
                    update_field(
                        phi,
                        phi_gradient,
                        phi_laplacian,
                        phi_transfer,
                        phi_grad_lap_fourier,
                        phi_grad_lap,
                        layouts,
                        force_on_grid,
                        hamiltonian,
                        pm,
                        positions,
                        types,
                        config,
                        v_ext,
                        phi_fourier,
                        phi_lap_filtered_fourier,
                        v_ext_fourier,
                        phi_lap_filtered,
                        v_ext1,
                        config.m,
                        compute_potential=True,
                    )
                    (
                        field_energy, kinetic_energy,
                    ) = compute_field_and_kinetic_energy(
                        phi, phi_gradient, velocities, hamiltonian, positions, types, v_ext,
                        config, layouts, comm=comm,
                    )

                    if charges_flag:
                        if config.coulombtype == "PIC_Spectral_GPE":
                            field_q_energy = compute_field_energy_q_GPE(
                                config, phi_eps,
                                field_q_energy,elec_dot,
                                comm=comm
                            )
                        if config.coulombtype == "PIC_Spectral":
                            field_q_energy = compute_field_energy_q(
                                config, phi_q_fourier, elec_energy_field,
                                field_q_energy, comm=comm,
                            )
                else:
                    kinetic_energy = comm.allreduce(
                        0.5 * config.mass * np.sum(velocities ** 2)
                    )
                temperature = (
                    (2 / 3) * kinetic_energy
                    / (config.gas_constant * config.n_particles)
                )
                if args.disable_field:
                    field_energy = 0.0

                if config.pressure:
                    pressure = comp_pressure(
                            phi,
                            phi_gradient,
                            hamiltonian,
                            velocities,
                            config,
                            phi_fourier,
                            phi_laplacian,
                            phi_transfer,
                            phi_grad_lap_fourier,
                            phi_grad_lap,
                            args,
                            bond_forces,
                            angle_forces,
                            positions,
                            bond_pr_,
                            angle_pr_,
                            Vbar_elec,
                            comm=comm
                    )
                else:
                    pressure = 0.0 #0.0 indicates not calculated. To be changed.

                forces_out = (
                    field_forces + bond_forces + angle_forces
                    + dihedral_forces + reconstructed_forces
                )
                store_data(
                    out_dataset, step, frame, indices, positions, velocities,
                    forces_out, config.box_size, temperature, pressure, kinetic_energy,
                    bond_energy, angle_energy, dihedral_energy, field_energy,
                    field_q_energy, config.respa_inner * config.time_step,
                    config, velocity_out=args.velocity_output,
                    force_out=args.force_output, charge_out=charges_flag,
                    dump_per_particle=args.dump_per_particle, comm=comm,
                )
                if np.mod(step, config.n_print * config.n_flush) == 0:
                    out_dataset.flush()
        last_step_time = current_step_time

    # End simulation
    if rank == 0:
        end_time = datetime.datetime.now()
        sim_time = end_time - start_time
        setup_time = loop_start_time - start_time
        loop_time = end_time - loop_start_time
        Logger.rank0.log(
            logging.INFO,
            (
                f"Elapsed time: {format_timedelta(sim_time)}   "
                f"Setup time: {format_timedelta(setup_time)}   "
                f"MD loop time: {format_timedelta(loop_time)}"
            ),
        )

    if config.n_print > 0 and np.mod(config.n_steps - 1, config.n_print) != 0:
        if not args.disable_field:
            update_field(
                phi,
                phi_gradient,
                phi_laplacian,
                phi_transfer,
                phi_grad_lap_fourier,
                phi_grad_lap,
                layouts,
                force_on_grid,
                hamiltonian,
                pm,
                positions,
                types,
                config,
                v_ext,
                phi_fourier,
                phi_lap_filtered_fourier,
                v_ext_fourier,
                phi_lap_filtered,
                v_ext1,
                config.m,
                compute_potential=True,
            )
            field_energy, kinetic_energy = compute_field_and_kinetic_energy(
                phi,
                phi_gradient,
                velocities,
                hamiltonian,
                positions,
                types,
                v_ext,
                config,
                layouts,
                comm=comm,
            )

            if charges_flag:
                layout_q = pm.decompose(positions)
                if config.coulombtype == "PIC_Spectral_GPE":
                    Vbar_elec, phi_eps, elec_dot = update_field_force_q_GPE(
                        conv_fun, phi, types, charges, config_charges,
                        phi_q, phi_q_fourier, phi_eps, phi_eps_fourier,
                        phi_eta,
                        phi_eta_fourier, phi_pol_prev, phi_pol,
                        elec_field, elec_forces, elec_field_contrib, elec_potential,
                        Vbar_elec, Vbar_elec_fourier, force_mesh_elec, force_mesh_elec_fourier,
                        hamiltonian, layout_q, layouts, pm, positions, config, comm = comm,
                        )


                    field_q_energy =compute_field_energy_q_GPE(
                        config, phi_eps,
                        field_q_energy,elec_dot,
                        comm=comm
                    )

                if config.coulombtype == "PIC_Spectral":
                    update_field_force_q(
                        charges, phi_q, phi_q_fourier, elec_field_fourier,
                        elec_field, elec_forces, layout_q, pm, positions, config,
                    )

                    field_q_energy = compute_field_energy_q(
                        config, phi_q_fourier, elec_energy_field, field_q_energy,
                        comm=comm,
                    )

        else:
            kinetic_energy = comm.allreduce(
                0.5 * config.mass * np.sum(velocities**2)
            )
        frame = (step + 1) // config.n_print
        temperature = (
            (2 / 3) * kinetic_energy
            / (config.gas_constant * config.n_particles)
        )
        if args.disable_field:
            field_energy = 0.0

        if config.pressure:
            pressure = comp_pressure(
                    phi,
                    phi_gradient,
                    hamiltonian,
                    velocities,
                    config,
                    phi_fourier,
                    phi_laplacian,
                    phi_transfer,
                    phi_grad_lap_fourier,
                    phi_grad_lap,
                    args,
                    bond_forces,
                    angle_forces,
                    positions,
                    bond_pr_,
                    angle_pr_,
                    Vbar_elec,
                    comm=comm
            )
        else:
            pressure = 0.0 #0.0 indicates not calculated. To be changed.

        forces_out = (
            field_forces + bond_forces + angle_forces + dihedral_forces
            + reconstructed_forces
        )
        store_data(
            out_dataset, step, frame, indices, positions, velocities,
            forces_out, config.box_size, temperature, pressure, kinetic_energy,
            bond_energy, angle_energy, dihedral_energy, field_energy,
            field_q_energy, config.respa_inner * config.time_step, config,
            velocity_out=args.velocity_output, force_out=args.force_output,
            charge_out=charges_flag, dump_per_particle=args.dump_per_particle,
            comm=comm,
        ) ## added pressure after temperature

    out_dataset.close_file()