from django import forms

class UploadForm(forms.Form):
    file_sub = forms.FileField(label='Choose a file to submit')
    
