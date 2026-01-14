from django import forms
from .models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['lettre_motivation', 'cv_personnalise']
        widgets = {
            'lettre_motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Bonjour, je suis très intéressé par...'
            }),
            'cv_personnalise': forms.FileInput(attrs={'class': 'form-control'}),
        }