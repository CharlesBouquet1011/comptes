from django import forms

class UploadCSVForm(forms.Form):
    titre=forms.CharField(max_length=50)
    fichier=forms.FileField()
    