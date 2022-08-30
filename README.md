# Electrostatics in Mesoscale Simulations of Biological Membranes using the Hybrid-Particle Field Approach

## Simulation and analysis of biological model systems with HyMD
Hello there, and welcome to this Github-page, which is dedicated to the code relevant for my thesis, completing the degree M.sc. Computational Science: Physics (2020-2022). The title of my thesis is: *Electrostatics in Mesoscale Simulations of Biological Membranes using the Hybrid-Particle Field Approach*.

<a href="https://cascella-group-uio.github.io/HyMD/">
  <img src="https://github.com/Cascella-Group-UiO/HyMD/blob/main/docs/img/hymd_logo_text_black.png?raw=true" width="500" title="HylleraasMD">
</a>


### Main overview
* This repository contains programmes used in the simulation and analysis of biological model systems of Lipid A hexa (LA6) and Lipid Re penta (LPS Re), which is both chemical components  of the outer membrane lipopolysaccharides in gram negative (GN) bacteria. LA6 is responsible for triggering host immune response, and the LPS is also known to make GN bacteria resistant to antimicrobial drugs. The LPS OM is reliant on a fine balanse between hydration and  stabilization of counter-ions to remain in a stable lamellar structure.
* Here, I develop an iterative method for solving a general Poisson equation (GPE) in the HylleraasMD ([HyMD](https://github.com/Cascella-Group-UiO/HyMD)) molecular dynamics platform. Adding this framework to the HyMD platform, opens up for simulating systems with an anisotropic (spatially dependent) permittivity, also called relative dielectric. In particular, anisotropic permittivity is of high relevance to biomolecular systems. 
* The Hylleraas platform is associated with the [Hylleraas Centre for Quantum Molecular Sciences](https://www.mn.uio.no/hylleraas/english/) at the University of Oslo. It implements the Hamiltonian formalism of the hybrid particle-field, and is a software applied to simulate coarse-grained models of softmatter systems in the canonical and isothermal–isobaric (in-preparation) ensembles. HyMD uses [PMESH](https://github.com/rainwoodman/pmesh) backend with fast Fourier transforms for parallel architectures.

<b href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/LA6-cg-mapping-pic-kopi.png?raw=true" width="300" title="Lipid A hexa">
</b>

<b href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/L-re5-cg-mapping-la6built-pic-kopi.png?raw=true" width="300" title="Lipid Re penta">
</b>

<b href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/la6-GPE-BO-all-kopi.png?raw=true" width="300" title="LA6-sim-example">
</b>

<b href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/epsilon_r-crop2.png?raw=true" width="300" title="variable dielectric">
</b>


### Thesis Abstract
> I develop and apply an iterative method to solve a general Poisson equation in Fourier space, with a variable dielectric. The iterative method is implemented in the molecular dynamics software HylleraasMD, using the Hamiltonian hPF formalism.

> First, I benchmark the iterative method with known cases. The method reproduces the electrostatic potential from an analytically constructed charge number density. When comparing with the Coulomb interaction of point particles, the iterative method yields reasonable magnitudes in force and energy, and momentum and energy are conserved. In addition, the method reproduces the behaviour of a 5mM electrolytic solution, with ideal monovalent ions dissolved in a biphase of liquid oil and water. 

> Secondly, I simulate systems of Lipid A and Lipid Re with divalent counter-ions in the NVT ensemble, applying two constant dielectric values and two variable dielectric functions. Results are benchmarked with density profiles  of all-atom simulations of the same systems. Model membranes of Lipid A and Lipid Re are in agreement with the reference membrane, except for low relative dielectric values, implying screening from polar moieties is necessary to preserve a lamellar bilayer. 

> Lastly, I optimize Flory Huggins mixing parameters with Bayesian optimization, for Lipid A. Optimization increase R2-fitness and reduce RMSE-scores, with no significant differences between trajectories for chosen dielectric parameters. Transferred to Lipid Re, optimized parameters give an improvement in R2 and RMSE compared to unoptimized parameters sets, except for the oligosaccharide chain, which is not present in Lipid A.


### Summary of contributions
My contributions can be summarized as follows:

- Development in HyMD and validation
    1. Develop an iterative method to solve a general Poisson equation (GPE) in Fourier Space in the HylleraasMD software.
    2. Validate the iterative method, and the HyMD implementation, against known cases, which include
    \begin{enumerate}
        - Solving a GPE with a Gaussian electrostatic potential, and test stability of convergence for different sets of method parameters.
        - Validating the Coulomb interaction between oppositely charged ideal ions.
        - Reproducing the partition of ions in a biphase of oil and water, with 5mM concentration.

- Application on LA6 and lipid Re model systems with divalent cations
    1. Compare variable dielectric results from simulations of biological model systems to constant dielectric simulations in the NVT ensemble. If the results with a variable dielectric corresponds better with the AA reference compared to a constant dielectric, there is a qualitative advantage to the new addition to the code. Specifically, it might indicate that a variable dielectric is necessary to reproduce the behaviour of electrochemically anistropic systems in coarse grain simulations.
    2. Optimize Flory Huggins mixing parameters for LA6 with divalent counter-ions in the NVT ensemble with Bayesian optimization. If successfull, this means one can optimize mixing parameters in the NVT ensemble, to obtain a better model description of bilayers containing LA6.
    3. After optimization, test transferability of optimized parameters on the LPS-Re model system with divalent cations in the NVT ensemble. If the results improve concordance with AA-simulations, it means that optimized parameters can be applied to chemically similar model systems.


### Code: Link and description of folders and programmes
- [HyMD-LS-cp](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/HyMD-LS-cp) : This is my version of HyMD, where I implement the iterative GPE solver. My contributions are mainly in the folder hymd, more specifically in
  1. [main.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/hymd/main.py) : Runs the MD integrations with or without variable dielectric electrostatics, depending on toml input specifications.
  2. [field.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/hymd/field.py) : Defines forces and energy functions on grid with more. 
  3. [input_parser.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/hymd/input_parser.py) :  Reads off the input tomli file and check that correct/needed input is given correctly.
  4. [file_io.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/hymd/file_io.py) : File input and output. Stores static and dynamic variables to HDF5 trajectory file.
  - The folder [utils](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/HyMD-LS-cp/utils) includes programmes with information on the LA6 molecule, and scripts used by the BO-optimization. These scripts are 1)  [change_chi.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/change_chi.py), 2) [get_next_point.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/get_next_point.py) 3) [get_next_point_random.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/get_next_point_random.py) 4) [hymd_optimize.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/hymd_optimize.py) 5) [write_to_opt_file_parallel.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/write_to_opt_file_parallel.py) 6) [read_parameter_file.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/read_parameter_file.py)
  
 - [Validation-and-analysis](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis) : Contains folders for analysing and benchmarking the iterative GPE method. 
  1. [analytical-case](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis/analytical-case) : Here, I construct an expression for the electrostatic potential, and define a variable dielectric function. From the forementioned functions, I derive at a charge density. I enter the charge density into the iterative method to check if the electrostatic potential is reproduced, and check how the results vary with different parameters.
  2. [coulomb](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis/coulomb) : I apply HyMD with the Poisson equation framework and the GPE framework I implemented to simulate two oppositely charged particles. Here, I compare the results with point particles Coulomb interaction, and the analytical expression for energy arising from two gaussian charge distributions.


  
### Protocols
#### HyMD-elec-GPE protocol
<d href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/elec-HyMD-kopi.png"?raw=true" width="300" title="HyMD-protocole">
</d>

#### Bayesian optimization protocol
<e href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/BO-flow-choice-kopi.png"?raw=true" width="300" title="HyMD-BO-protocole">
</e>



