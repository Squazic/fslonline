from django.db import models
from django.core.files.storage import FileSystemStorage

stor = FileSystemStorage()
# Create your models here.

class UploadFile(models.Model):
    title = models.CharField(max_length=50)
    file_sub  = models.FileField(upload_to='uploads')

