from subprocess import call
import os
import nipype.interfaces.fsl as fsl
import sys

def run_bet(infile, outfile):
    """
    Does analysis Make sure FSL is installed correctly and the configure
    options are selected. In linux, your .bashrc should have something
    like the follwing:
    export PATH=$PATH:/home/chenst/mipav
    export NIPYPE_NO_MATLAB=
    export FSLOUTPUTTYPE=NIFTI_GZ
    
    FSLDIR=/usr/share/fsl
    . ${FSLDIR}/4.1/etc/fslconf/fsl.sh
    PATH=${FSLDIR}/bin:${PATH}
    export FSLDIR PATH
    """
    mybet = fsl.BET()
    mybet.inputs.in_file = infile
    mybet.inputs.out_file = outfile
    result = mybet.run()

def extract_gz(filename):
    """ Extracts .gz """
    call(["gzip", "-df", filename])

def nii2jpg(filename, sctfile):
    """ Converts nii to jpg.  The sct file can be make by opening up
    mipav and turning on script logging while exporting a file to a
    certain format. Here that's, .jpg"""
    call(["mipav", "-i", filename, "-s", sctfile, "-hide"])
