# Automated Relaxation of Materials with DFTB+
This repository contains scripts written by A. Davies and T. Kelsey to automate the relaxation of structures using the package, DFTB+. The current form of these scripts is written to work on the UWyo ARCC HPC, MedicineBow. If the HPC environment changes, be sure to follows the changes in [If the HPC environment changes...](#if-the-hpc-environment-changes). Be sure to copy all files in [bin](https://github.com/ADavies2/Auto-DFTB-Relax/tree/main/bin) into your personal bin and make them executable.

This script is currently *only* written to work with the 3ob-3-1 parameter set. If you would like to run a calculation using a different parameter set or using extended tight-binding, you will need to edit **auto-relax.sh** yourself. 

The primary automation is done by the bash script, **auto-relax.sh**. The structure in question is iteratively relaxed over four sequences starting from a SCC (eV)/Force (eV/Å) tolerance of 1e-1. The second sequence uses a SCC/Force tolerance of 1e-2. The third sequence uses a SCC/Force tolerance of 1e-3. The final sequence uses a SCC tolerance of 1e-5 and a Force tolerance of 1e-4. After each sequence is complete, a directory will be made titled **{TOL}-Outputs**. For instance, the directory containing the 1e-1 tolerance results is called **1e-1-Outputs**. The results stored in each directory are:
- charges.bin
- {TOL}.gen
- detailed.out
- submit_{COF}-scc-{TOL}
- {COF}-scc-{TOL}.log

**auto-relax.sh** also automatically calculates desired properties of the final structure. These properties are, including their output filename:
- The atomic densities ({COF}.densities)
- The cohesive energy and enthalpy of formation (Energies.dat)
- Pore diameters, surface areas, and volumes ({COF}.res, {COF}.sa, and {COF}.vol)

For a finished calculation, the final directory (1e-4-Outputs) will contain:
- charges.bin
- 1e-4-Out.gen
- 1e-4-Out.xyz
- charges.dat 
- detailed.out
- detailed.xml 
- eigenvec.bin
- {COF}-scc-1e-4.log
- band.out 
- {COF}-Out-POSCAR
- {COF}.densities
- Energies.dat
- {COF}.res
- {COF}.sa
- {COF}.vol
- OUTPUT.zeo

A file called **{BASH-JOBNAME}.out** will contain "status" report and SLURM JOBID for each sequence of the calculation.

This script can be executed by running the following command: <code>auto-relax.sh relax.in {BASH-JOBNAME}</code>. 

*PLEASE* use a submit script to submit this job to your queue manager. *DO NOT RUN IT IN COMMAND LINE VIA A LOG IN NODE.* [An example submit script](https://github.com/ADavies2/Auto-DFTB-Relax/tree/main/submit_auto-relax) has been provided for your guidance.

**auto-relax.sh** automatically generates the following files based on the user input into **relax.in**:
1. dftb_in.hsd 
2. submit_{COF}-scc-{TOL}
This means that the only files the user must support are the initial structure file and **relax.in**. The other necessary files will be generated by either **auto-relax.sh** or by DFTB+ for the following runs. 

An example calculation, along with output files, has been included in the directory [example](https://github.com/ADavies2/Auto-DFTB-Relax/tree/main/submit_auto-relax/example/).

## Relax.in

 [An example relax.in](https://github.com/ADavies2/Auto-DFTB-Relax/tree/main/submit_auto-relax/example/relax.in) has been provided for your guidance. **relax.in** should contain 5 lines with only the information that you desire on them. Do not include comments on each line as the current version of auto-relax.sh does not know how to interpret these.

- The COF_NAME must be the name of your COF with word separations made only by hyphens or underscores, no spaces.
- The INITIAL_TOLERANCE may be any setting between 1e-1 and 1e-4. If 1e-4 is given, **auto-relax.sh** will automatically set Forces = 1e-4 and SCC = 1e-5. 
- The INITIAL_STRUCTURE_FILE is the filename that contains your initial structure coordinates. POSCAR or .gen file types are recommended against .xyz types as DFTB+ does not read extended .xyz formats, meaning that the simulation cell parameters will not be included. 
If the user has a previously converged charges.bin file for this system, they can initialize the DFTB+ calculation from that charges.bin file by setting RESTART to yes. If the user does not have a charges.bin file (i.e., this is a calculation from scratch), set RESTART to no.
- Give the desired partition name for the calculations to run on (mb, teton, inv-desousa, etc.).
- STACKING_CONFIGURATION will specify if the simulation cell angles will be fixed during the relaxation. Use this setting if you do not want the layers of your system to "slip", which is typically for AB-Stagg, ABC, or AA-Eclipse geometries. If you are modelling one of these three configurations, specify on this line either AB-Stagg, ABC, or AA-Eclipsed. If you are not running one of these three geometries or do not want the simulation cell angles fixed, leave this line empty or type None.

## If the HPC environment changes...

If you would like to run this script on a different HPC enviornment, you will need to change the following lines within **auto-relax.sh**

- Line 128: <code>Prefix = "/project/design-lab/software/DFTB+/3ob-3-1/"</code>
    - Update the path to correctly point to your Slater-Koster files. 
- Lines 199-202: <code>module load miniconda3/24.3.0 ... conda deactivate</code>
    - Update the lines from 199-202 to correctly load and execute DFTB+. This version was built with a Conda enviornment.
- Lines 243/245/247: <code>~/Software/zeo++-0.3/network...</code>
    - Update lines 243, 245 and 247 to include the correct path to your Zeo++ executable. 
- Line 373: <code>module load gcc/14.2.0 python/3.12.0</code>
    - Update this line to load the appropriate modules required for running Python on your HPC.

## Known Issues

- DFTB+ is known to "stall" on the MedicineBow HPC. When this happens, the calculation continues taking up time on the clock, but no data is written to the output files. **auto-relax.sh** attempts to account for this by checking for file size changes, and if the file size has not changed in 3 minutes, it assumes the job has stalled and kills the current iteraction job. Then, it uses the .gen produced from this iteration as the new input, lowers the number of tasks-per-node, and resubmits the calculation to restart from the last written point. It will be noted in **{BASH-JOBNAME}.out** when a job has stalled. 
    - Sometimes, this can happen at the very beginning of the calculation before any data is written to the {TOL}.gen file. When this happens, **auto-relax.sh** will still tell DFTB+ to read this .gen file as the next input, but DFTB+ will crash because there is no data in the .gen file.
    - To circumnavigate this, instead of running from your current tolerance, for instance, if the job stalls at the first step of the 1e-1 iteration, changed **relax.in** to start from the next iteration, i.e., 1e-2. This usually fixes the problem and the calculation will continue running. Note, though, that this will not generate a 1e-1-Outputs directory, as this iteration has been skipped.