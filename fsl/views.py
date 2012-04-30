from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, shutil
from nii2jpg import run_bet, extract_gz, nii2jpg
from django.conf import settings
from operator import itemgetter

def index(request):
    return render_to_response('fsl/index.html', {'message': 'w00T'})

def run_fsl(request, file_name):
    folder = settings.MEDIA_ROOT
    infile = file_name + ".nii"

    if infile[-4:] != ".nii":
        raise NameError('Filename incorrect!')

    nii_file = os.path.join("fsl", infile)
    # Creates directory to hold new files, deletes dir if already exists
    new_dir = os.path.join(folder, file_name)
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)
    nii_outfile = os.path.join(new_dir, file_name + "_out.nii")

    # Runs FSL
    run_bet(nii_file, nii_outfile)
    extract_gz(nii_outfile + ".gz")
    sctfile = os.path.join(os.getcwd(), "fsl", "nii2jpg.sct")
    nii2jpg(nii_outfile, sctfile)

    # Displys output images, starting with first one
    return disp_fsl(request, file_name, 1)

def disp_fsl(request, file_name, num):
    folder = settings.MEDIA_ROOT
    new_dir = os.path.join(folder, file_name)

    # Gets lits of images from the proper media subdir
    sorted_imgs = [img[-7:-4] for img in os.listdir(new_dir) \
                       if img[-4:] == ".jpg"]
    sorted_imgs.sort()

    # Displays the correct one
    imgfile = file_name + "_out%03d.jpg" % int(num)
    imgurl = os.path.join(settings.MEDIA_URL, file_name, imgfile)

    return render_to_response('fsl/display.html', \
                                  {'imgname': imgurl, 'filelist': sorted_imgs})
