from django import forms
from .models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['lettre_motivation', 'cv_personnalise']
        widgets = {
            'lettre_motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cv_personnalise': forms.FileInput(attrs={'class': 'form-control'}),
        }