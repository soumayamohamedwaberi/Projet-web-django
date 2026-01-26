from django import forms
from django.contrib.auth.models import User
# 👇 C'EST ICI LA CORRECTION : On importe bien OffreStage et Candidature
from .models import Candidature, OffreStage 

# ============================================================
# 1. FORMULAIRE DE CANDIDATURE (Pour les étudiants)
# ============================================================
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv', 'lettre_motivation']
        labels = {
            'cv': 'Votre CV (PDF)',
            'lettre_motivation': 'Lettre de motivation',
        }
        widgets = {
            'lettre_motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
        }

# ============================================================
# 2. FORMULAIRE INSCRIPTION ÉTUDIANT
# ============================================================
class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    telephone = forms.CharField(label="Téléphone", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    niveau = forms.CharField(label="Niveau d'études", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialite = forms.CharField(label="Spécialité", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

# ============================================================
# 3. FORMULAIRE INSCRIPTION ENTREPRISE
# ============================================================
class CompanyRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur (Login)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email professionnel", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    nom_entreprise = forms.CharField(label="Nom de l'entreprise", widget=forms.TextInput(attrs={'class': 'form-control'}))
    secteur = forms.CharField(label="Secteur d'activité", widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(label="Adresse", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    site_web = forms.URLField(label="Site Web", required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label="Téléphone", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

# ============================================================
# 4. FORMULAIRE CRÉATION OFFRE (Pour les entreprises)
# ============================================================
class OffreForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        fields = ['titre', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }