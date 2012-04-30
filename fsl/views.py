from django.http import HttpResponse
from django.shortcuts import render_to_response
import os, shutil
from nii2jpg import run_bet, extract_gz, nii2jpg
from django.conf import settings
from operator import itemgetter

from django.template import RequestContext
from fsl.models import UploadFile
from fsl.forms import UploadForm
from django.core.urlresolvers import reverse
from django.template import Context, loader


def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file_sub = request.FILES['file_sub'])
            new_file.save()
            file_in = new_file.file_sub
            subs = UploadFile.objects.all()
            file_name = file_in.name.split("/")[-1]
            return render_to_response('fsl/redirect.html', \
                                          {'subs': subs, 'form': form, \
                                               'file_in': file_in, \
                                               'url': file_name},
                              context_instance=RequestContext(request))


    else:
        form = UploadForm()
        subs = UploadFile.objects.all()
        return render_to_response('fsl/home.html', {'subs': subs, 'form': form},
                              context_instance=RequestContext(request))


def run_fsl(request, file_name):
    """ Runs FSL Scripts """
    if file_name[-4:] != ".nii":
        raise NameError('Filename incorrect!')

    media_root = settings.MEDIA_ROOT
    infile = file_name[:-4] + "_in.nii"
    nii_file = os.path.join(media_root, "uploads", file_name)

    # Creates directory to hold new files, deletes dir if already exists
    outfile_dir = os.path.join(media_root, file_name)
    if os.path.isdir(outfile_dir):
        shutil.rmtree(outfile_dir)
    os.mkdir(outfile_dir)
    # Dir for uploaded file
    infile_dir = os.path.join(media_root, infile)
    if os.path.isdir(infile_dir):
        shutil.rmtree(infile_dir)
    os.mkdir(infile_dir)
    shutil.copy(nii_file, infile_dir)
    nii_infile = os.path.join(infile_dir, file_name)

    nii_outfile = os.path.join(outfile_dir, file_name[:-4] + "_out.nii")

    # Runs FSL
    print infile_dir
    print os.path.join(infile_dir)
    print os.path.join(infile_dir, nii_file)
    print nii_infile
    run_bet(nii_infile, nii_outfile)
    extract_gz(nii_outfile + ".gz")
    sctfile = os.path.join(os.getcwd(), "fsl", "nii2jpg.sct")
    nii2jpg(nii_outfile, sctfile)
    nii2jpg(nii_infile, sctfile)

    # Displys output images, starting with first one
    return disp_fsl(request, file_name, 1)

def disp_fsl(request, file_name, num):
    if file_name[-4:] != ".nii":
        raise NameError('Filename incorrect!')

    media_root = settings.MEDIA_ROOT

    # Gets list of processed images from the proper media subdir
    outfile_dir = os.path.join(media_root, file_name)
    sorted_imgs = [img[-7:-4] for img in os.listdir(outfile_dir) \
                       if img[-4:] == ".jpg"]
    sorted_imgs.sort()

    # Gets list of original images from the proper media subdir
    infile = file_name[:-4] + "_in.nii"
    infile_dir = os.path.join(media_root, infile)
    in_imgs = [img[-7:-4] for img in os.listdir(infile_dir) \
                       if img[-4:] == ".jpg"]
    in_imgs.sort()

    # Displays the correct one
    imgfile = file_name[:-4] + "_out%03d.jpg" % int(num)
    imgurl = os.path.join(settings.MEDIA_URL, file_name, imgfile)

    # Displays the correct one
    in_img_file = file_name[:-4] + "%03d.jpg" % int(num)
    inurl = os.path.join(settings.MEDIA_URL, infile, in_img_file)

    return render_to_response('fsl/display.html', \
                                  {'imgname': imgurl, \
                                       'filelist': sorted_imgs, \
                                       'imgin': inurl, \
                                       'infiles': in_imgs})
