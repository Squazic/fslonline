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
    if file_name[-4:] != ".nii":
        raise NameError('Filename incorrect!')

    media_root = settings.MEDIA_ROOT

    infile = file_name

    nii_file = os.path.join(media_root, "uploads", infile)
    print nii_file
    # Creates directory to hold new files, deletes dir if already exists
    new_dir = os.path.join(media_root, file_name)
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)
    nii_outfile = os.path.join(new_dir, file_name[:-4] + "_out.nii")

    # Runs FSL
    run_bet(nii_file, nii_outfile)
    extract_gz(nii_outfile + ".gz")
    sctfile = os.path.join(os.getcwd(), "fsl", "nii2jpg.sct")
    nii2jpg(nii_outfile, sctfile)

    # Displys output images, starting with first one
    return disp_fsl(request, file_name, 1)

def disp_fsl(request, file_name, num):
    if file_name[-4:] != ".nii":
        raise NameError('Filename incorrect!')

    media_root = settings.MEDIA_ROOT
    new_dir = os.path.join(media_root, file_name)
    print new_dir
    # Gets lits of images from the proper media subdir
    sorted_imgs = [img[-7:-4] for img in os.listdir(new_dir) \
                       if img[-4:] == ".jpg"]
    sorted_imgs.sort()
    print sorted_imgs
    # Displays the correct one
    imgfile = file_name[:-4] + "_out%03d.jpg" % int(num)
    imgurl = os.path.join(settings.MEDIA_URL, file_name, imgfile)

    return render_to_response('fsl/display.html', \
                                  {'imgname': imgurl, 'filelist': sorted_imgs})
