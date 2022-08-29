# Simulation and analysis of biomolecular model systems with HyMD

Hello there, and welcome to this Github-page, which is dedicated to the code relevant for my thesis, completing the degree M.sc. Computational Science: Physics (2020-2022).

### Main overview:
* This repository contains programmes used in the simulation and analysis of biological model systems of Lipid A hexa (LA6) and Lipid Re penta (LPS Re), which is both chemical components  of the outer membrane lipopolysaccharides in gram negative (GN) bacteria. LA6 is responsible for triggering host immune response, and the LPS is also known to make GN bacteria resistant to antimicrobial drugs. The LPS OM is reliant on a fine balanse between hydration and  stabilization of counter-ions to remain in a stable lamellar structure.
* Here, I develop an iterative method for solving a general Poisson equation in the HylleraasMD ([HyMD](https://github.com/Cascella-Group-UiO/HyMD)) molecular dynamics platform. 
* The Hylleraas platform is associated with the [Hylleraas Centre for Quantum Molecular Sciences](https://www.mn.uio.no/hylleraas/english/). It implements the Hamiltonian formalism of the hybrid particle-field, and is a software applied to simulate coarse-grained models of softmatter systems in the canonical and isothermal–isobaric (in-preparation) ensembles. HyMD uses [PMESH](https://github.com/rainwoodman/pmesh) backend with fast fourier transforms for parallel architectures.

<a href="https://cascella-group-uio.github.io/HyMD/">
  <img src="https://github.com/Cascella-Group-UiO/HyMD/blob/main/docs/img/hymd_logo_text_black.png?raw=true" width="500" title="HylleraasMD">
</a>

### Thesis Abstract
> I develop and apply an iterative method to solve a general Poisson equation in Fourier space, with a variable dielectric. The iterative method is implemented in the molecular dynamics software HylleraasMD, using the Hamiltonian hPF formalism.

> First, I benchmark the iterative method with known cases. The method reproduces the electrostatic potential from an analytically constructed charge number density. When comparing with the Coulomb interaction of point particles, the iterative method yields reasonable magnitudes in force and energy, and momentum and energy are conserved. In addition, the method reproduces the behaviour of a 5mM electrolytic solution, with ideal monovalent ions dissolved in a biphase of liquid oil and water. 

> Secondly, I simulate systems of Lipid A and Lipid Re with divalent counter-ions in the NVT ensemble, applying two constant dielectric values and two variable dielectric functions. Results are benchmarked with density profiles  of all-atom simulations of the same systems. Model membranes of Lipid A and Lipid Re are in agreement with the reference membrane, except for low relative dielectric values, implying screening from polar moieties is necessary to preserve a lamellar bilayer. 

> Lastly, I optimize Flory Huggins mixing parameters with Bayesian optimization, for Lipid A. Optimization increase R2-fitness and reduce RMSE-scores, with no significant differences between trajectories for chosen dielectric parameters. Transferred to Lipid Re, optimized parameters give an improvement in R2 and RMSE compared to unoptimized parameters sets, except for the oligosaccharide chain, which is not present in Lipid A.


### Summary of contributions
My contributions can be summarized as follows:
A detailed overview of my contribution is given below.
- 
  1. init: Sets up member parameters and vectors by calling the superclass method initialize from finitediffs.cpp.
  2. set_initial: Initializes the solution vector u_n with zero everywhere, except at the boundaries. The boundaries are set to u_n(0) = 0 and u_n(Nx) = 1. 
  3. advance: Moving the system to a new moment in time and calculates the new solution vector u, except at the boundaries which are fixed during the entire       simulation.
  4. solve: Advances the system multiple moments in time by calling the method advance Nt times. For every advancement the corresponding solutions are written to file.
  5. The other methods provided are write to file methods.

- Development in HyMD and validation
    1. Develop an iterative method to solve a general Poisson equation (GPE) in Fourier Space in the HylleraasMD software.
    2. Validate the iterative method, and the HyMD implementation, against known cases, which include
    \begin{enumerate}
        - Solving a GPE with a Gaussian electrostatic potential, and test stability of convergence for different sets of method parameters.
        - Validating the Coulomb interaction between oppositely charged ideal ions.
        - Reproducing the partition of ions in a biphase of oil and water, with 5mM concentration.

- Application on LA6 and lipid Re model systems with divalent cations
    1. Compare variable dielectric results from simulations of biological model systems to constant dielectric simulations in the NVT ensemble. If the results with a variable dielectric corresponds better with the AA reference compared to a constant dielectric, there is a qualitative advantage to the new addition to the code. Specifically, it might indicate that a variable dielectric is necessary to reproduce the behaviour of electrochemically anistropic systems in coarse grain simulations.
    2. Optimize Flory Huggins mixing parameters for LA6 with Ca$^{2+}$ in the NVT ensemble with Bayesian optimization. If successfull, this means one can optimize mixing parameters in the NVT ensemble, to obtain a better model description of bilayers containing LA6.
    3. After optimization, test transferability of optimized parameters on the LPS-Re model system with Ca$^{2+}$ in the NVT ensemble. If the results improve concordance with AA-simulations, it means that optimized parameters can be applied to chemically similar model systems.

### Code: Link and description of programmes

### Links and packages



