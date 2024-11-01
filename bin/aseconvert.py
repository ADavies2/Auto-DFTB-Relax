#!/usr/bin/env python
# AUTHOR: ALATHEA DAVIES

import ase.io

InputFile = input('What is the name of your input file? ')
if 'gen' in InputFile:
    InputData = ase.io.read(InputFile, format='gen')
    print('gen input')
elif 'cif' in InputFile:
    InputData = ase.io.read(InputFile, format='cif')
    print('cif input')
elif 'data' in InputFile:
    InputData = ase.io.read(InputFile, format='lammps-data')
    print('LAMMPS data input')
elif 'POSCAR' or 'vasp' or 'CONTCAR' in InputFile:
    InputData = ase.io.read(InputFile, format='vasp')
    print('vasp input')

OutputFile = input('What would you like to call your converted file? ')
if 'gen' in OutputFile:
    ase.io.write(OutputFile, images=InputData, format='gen')
    print('gen output')
elif 'cif' in OutputFile:
    ase.io.write(OutputFile, images=InputData, format='cif')
    print('cif output')
elif 'POSCAR' or 'vasp' in OutputFile:
    ase.io.write(OutputFile, images=InputData, format='vasp')
    print('POSCAR output')