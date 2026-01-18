from django import forms
from .models import Candidature, OffreStage

# ---------------------------------------------------------
# 1. TON FORMULAIRE (Pour les étudiants)
# ---------------------------------------------------------
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
    
    # Validation personnalisée pour la taille du fichier (Ton bonus)
    def clean_cv_personnalise(self):
        cv = self.cleaned_data.get('cv_personnalise')
        if cv:
            if cv.size > 5 * 1024 * 1024: # 5 Mo
                raise forms.ValidationError("Le fichier est trop lourd (Max 5Mo)")
        return cv

# ---------------------------------------------------------
# 2. LE FORMULAIRE DE TES COLLEGUES (Pour les entreprises)
# ---------------------------------------------------------
class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        # On demande juste le titre et la description
        # L'entreprise est remplie automatiquement par le système, pas par l'utilisateur
        fields = ['titre', 'description'] 
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Développeur Python'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }