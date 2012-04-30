Welcome to FSLOnline, an online interface for FSL

To get started:

Download [MIPAV](http://mipav.cit.nih.gov) and install it in a
directory called `mipav` in your home folder.

Download [FSL](http://www.fmrib.ox.ac.uk/fsl/) and make sure it is configured properly. On Ubuntu 10.10, you can run `sudo apt-get install fsl`
and then make sure the following is in your `.bashrc`
    
    export PATH=$PATH:~/mipav
    export NIPYPE_NO_MATLAB=
    export FSLOUTPUTTYPE=NIFTI_GZ
    
    FSLDIR=/usr/share/fsl
    . ${FSLDIR}/4.1/etc/fslconf/fsl.sh
    PATH=${FSLDIR}/bin:${PATH}
    export FSLDIR PATH
    
To run the program, start a django server with `python manage.py
runserver` in the root fslonline directory. Navigate to
http://127.0.0.1:8000/fsl to begin.