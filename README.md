# Electrostatics in Mesoscale Simulations of Biological Membranes using the Hybrid Particle-Field Approach

## Simulation and analysis of biological model systems with HyMD
Hello there, and welcome to this Github-page, which is dedicated to the code relevant for my thesis, completing the degree M.sc. Computational Science: Physics (2020-2022) at the University of Oslo. The title of my thesis is: *Electrostatics in Mesoscale Simulations of Biological Membranes using the Hybrid Particle-Field Approach*.

<a href="https://cascella-group-uio.github.io/HyMD/">
  <img src="https://github.com/Cascella-Group-UiO/HyMD/blob/main/docs/img/hymd_logo_text_black.png?raw=true" width="500" title="HylleraasMD">
</a>


### Main overview
* This repository contains programmes used in the simulation and analysis of biological model systems of Lipid A hexa (LA6) and Lipid Re penta (LPS Re), which is both chemical components  of the outer membrane lipopolysaccharides in gram negative (GN) bacteria. LA6 is responsible for triggering host immune response, and the LPS is also known to make GN bacteria resistant to antimicrobial drugs. The LPS OM is reliant on a fine balanse between hydration and  stabilization of counter-ions to remain in a stable lamellar structure.
* Here, I develop an iterative method for solving a general Poisson equation (GPE) in the HylleraasMD ([HyMD](https://github.com/Cascella-Group-UiO/HyMD)) molecular dynamics platform. Adding this framework to the HyMD platform, opens up for simulating systems with an inhomogenous (spatially dependent) permittivity, also called relative dielectric. In particular, inhomogenous permittivity is of high relevance to biomolecular systems. 
* The Hylleraas platform is associated with the [Hylleraas Centre for Quantum Molecular Sciences](https://www.mn.uio.no/hylleraas/english/) at the University of Oslo. It implements the Hamiltonian formalism of the hybrid particle-field, and is a software applied to simulate coarse-grained models of softmatter systems in the canonical and isothermal???isobaric (in-preparation) ensembles. HyMD uses [PMESH](https://github.com/rainwoodman/pmesh) backend with fast Fourier transforms for parallel architectures.

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

> Secondly, I simulate systems of Lipid A and Lipid Re with divalent counter-ions in the NVT ensemble, applying two constant dielectric values and two variable dielectric functions. Results are benchmarked with density profiles  of united-atom simulations of the same systems. Model membranes of Lipid A and Lipid Re are in agreement with the reference membrane, except for low relative dielectric values, implying screening from polar moieties is necessary to preserve a lamellar bilayer. 

> Lastly, I optimize Flory Huggins mixing parameters with Bayesian optimization, for Lipid A. Optimization increase $R^2$-fitness and reduce RMSE-scores, with no significant differences between trajectories for chosen dielectric parameters. Transferred to Lipid Re, optimized parameters give an improvement in $R^2$ and RMSE compared to unoptimized parameters sets, except for the oligosaccharide chain, which is not present in Lipid A.


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

### Running HyMD
You can read more about how to install and run HyMD at Github [HyMD](https://github.com/Cascella-Group-UiO/HyMD).

### Code: Link and description of folders and programmes
- My version of HyMD will be available on this repository after an article has been published related to my work. 
  
 - [Validation-and-analysis](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis) : Contains folders for analysing and benchmarking the iterative GPE method. 
    1. [analytical-case](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis/analytical-case) : I construct an expression for the electrostatic potential, and define a variable dielectric function. From the forementioned functions, I derive at a charge density. I enter the charge density into the iterative method to check if the electrostatic potential is reproduced, and check how the results vary with different parameters.
    2. [coulomb](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/Validation-and-analysis/coulomb) : I apply HyMD with the Poisson equation framework and the GPE framework I implemented to simulate two oppositely charged particles. I compare the results with point particles Coulomb interaction, and the analytical expression for energy arising from two gaussian charge distributions.

- [example-trajectory-log-files](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/example-trajectory-log-files) : Some log files, which gives information on the toml-input and prompts of several parameters during trajectory runs. 

- [fitness-script-and-data](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/fitness-script-and-data) : Folder with fitness data for [LA6](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/fitness-script-and-data/LA6) and [LPS Re](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/fitness-script-and-data/LPS-Re), and the script used to obtain fitness data and density profiles 1) LA6 [hymd_optimize.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/fitness-script-and-data/LA6/hymd_optimize.py) 2) LPS Re [hymd_optimize.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/fitness-script-and-data/LPS-Re/hymd_optimize.py)
  
- [input-HDF5-and-tomli](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli): Input trajectory HDF5/H5 and input toml/tomli scripts for various systems:
  1. [LA6](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/LA6)  and [LA6-cropped](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/LA6-cropped)
  2. [LPS-Re](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/LPS-Re) and [LPS-Re-cropped](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/LPS-Re-cropped)
  3. [biphase](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/biphase), 5mM electrolytic solution oil and water partition. 
  4. [coulomb](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/coulomb), two oppositely charged CG beads. With water, but tomli is set so that water beads have no effect on charged beads (kappa high and interaction parameter 0). Having water in the system opens to for further investigation of behaviour with varying dielectric.
  5. [water-ions](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/input-HDF5-and-tomli/water-ions), 150mM electrolytic solution with only water as solvent. (Extra system).
  
- [job-scripts-examples](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/job-scripts-examples) : Relevant job script examples from (Saga)[https://documentation.sigma2.no/hpc_machines/saga.html] and (Betzy)[https://documentation.sigma2.no/hpc_machines/betzy.html] clusters at the high performance computing facility maintained by [the Norwegian Research Infrastructure Services](https://documentation.sigma2.no/index.html). 

- [mapping-and-gro-to-h5](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5) : Mapping and scripts to build input HDF5 trajectory files.  
  1. For [LA6](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5/bilayer-details) and [LPS Re](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5/bilayer-details) : From united-atom to coarse-grained representation, including transition from .gro to HDF5 input trajectory file. 
  2. [biphase](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5/biphase) : PACKMOL and gro to HDF5
  3. [coulomb](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5/coulomb) : PACKMOL and gro to HDF5
  4. [ions-water](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/mapping-and-gro-to-h5/ions-water) : PACKMOL and gro to HDF5. (Extra system)
  - The united-atom to CG mapping depends on a CG builder ([https://jbarnoud.github.io/cgbuilder/](https://jbarnoud.github.io/cgbuilder/)) as described in my thesis. Credit goes to Manuela Nader for doing the UA to CG mapping of LA6 and LPS Re.
  - The step gro to HDF5 is possible with the files .gro .inp and .itp describing the configuration, and the utils function [gmx_2_hymd.py](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/HyMD-LS-cp/utils/gmx_2_hymd.py).

- [opt-data](https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/tree/main/opt-data) : Txt-files with the raw optimization data and simple scripts to find the lowest SMAPE/R2 set of parameters. In addition, a modified version of a script provided by [Morten Ledum](https://github.com/mortele), used to analyse raw data to provide plots of F-values and data distributions (Morten also wrote a lot of the backbone to HyMD in its current state). 


### Protocols
#### HyMD-elec-GPE protocol
<d href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/elec-HyMD-kopi.png"?raw=true" width="300" title="HyMD-protocole">
</d>

#### Bayesian optimization protocol
<e href="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/">
  <img src="https://github.com/lasse-steinnes/Electrostatics-and-Biological-membranes-MT2022/blob/main/assets/BO-flow-choice-kopi.png"?raw=true" width="300" title="HyMD-BO-protocole">
</e>

## Acknowlegdement
First and foremost, I am grateful for the help and advice of my supervisor, Michele Cascella, and my co-supervisor, Morten Hjorth-Jenssen, who both made this project a possibility for me. The following people has also been of great support and importance to me in the process of my Master Thesis: Sidra Rashid - for shared laughs and struggles, Xinmeng Li - for getting me started, Samiran Sen, Morten Ledum, Marinella Guivanetti and Manuel Carrer. 

Acknowlegdment goes to Thereza Soares at the University of Sao Paulo, whose research group provided the united-atom reference frames, and to Manuela Nader, who was vital in the mapping of those into a coarse grain representation. 

Furthermore, I have been fortunate enough not only to be surrounded by intelligent, interesting and kind people, who make a consistent effort in contributing to the scientific community, but also being a part of two centres of Excellence during my master studies: The Center For Computing in Science Education and the Hylleraas Centre for Quantum Molecular Sciences. They both have excellent office and computing facilities. On that note, I would like to thank the National Infrastructure for Research Data ([NIRD](https://documentation.sigma2.no/files_storage/nird.html)), which has provided the high performance computing facilities I needed to finish this thesis. 


