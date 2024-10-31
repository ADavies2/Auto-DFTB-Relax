# Automated Relaxation of Materials with DFTB+
This repository contains scripts written by A. Davies and T. Kelsey to automate the relaxation of structures using the package, DFTB+. The current form of these scripts is written to work on the UWyo ARCC HPC, MedicineBow. If the HPC environment changes, be sure to follows the changes in [If the HPC environment changes...](#if-the-hpc-environment-changes). Be sure to copy all files in [bin][ADavies2/Auto-DFTB-Relax/bin/].

The primary automation is done by the bash script, **auto-relax.sh**. The structure in question is iteratively relaxed over four sequences starting from a SCC (eV)/Force (eV/Å) tolerance of 1e-1. The second sequence uses a SCC/Force tolerance of 1e-2. The third sequence uses a SCC/Force tolerance of 1e-3. The final sequence uses a SCC tolerance of 1e-5 and a Force tolerance of 1e-4. After each sequence is complete, a directory will be made titled **<tolerance>-Outputs**. For instance, the directory containing the 1e-1 tolerance results is called **1e-1-Outputs**. The results stored in each directory are:
- charges.bin
- <tolerance>.gen
- detailed.out
- submit_<COF>-scc-<tolerance>
- <COF>-scc-<tolerance>.log

**auto-relax.sh** also automatically calculates desired properties of the final structure. These properties are, including their output filename:
- The atomic densities (<COF>.densities)
- The cohesive energy and enthalpy of formation (Energies.dat)
- Pore diameters, surface areas, and volumes (<COF>.res, <COF>.sa, and <COF>.vol)

For a finished calculation, the final directory (1e-4-Outputs) will contain:
- charges.bin
- 1e-4-Out.gen
- 1e-4-Out.xyz
- charges.dat 
- detailed.out
- detailed.xml 
- eigenvec.bin
- <COF>-scc-1e-4.log
- band.out 
- <COF>-Out-POSCAR
- <COF>.densities
- Energies.dat
- <COF>.res
- <COF>.sa
- <COF>.vol
- OUTPUT.zeo

This script can be executed by running **auto-relax.sh relax.in** where **relax.in** is the input script. The format of **relax.in** is described in [Relax.in](#relaxin). **auto-relax.sh** automatically generates the following files based on the user input into **relax.in**:
1. dftb_in.hsd 
2. submit_<COF>-scc-<TOL>

# Relax.in

# If the HPC environment changes...

# Known Issues