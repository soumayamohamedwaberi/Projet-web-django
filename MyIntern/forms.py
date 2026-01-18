# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ProfilEtudiant, ProfilEntreprise


class InscriptionEtudiantForm(UserCreationForm):
    """
    Formulaire d'inscription pour les étudiants
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre.email@example.com'})
    )
    telephone = forms.CharField(
        max_length=15,
        required=False,
        label="Téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0612345678'})
    )
    niveau = forms.CharField(
        max_length=50,
        required=True,
        label="Niveau d'études",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2ème année'})
    )
    specialite = forms.CharField(
        max_length=100,
        required=True,
        label="Spécialité",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Génie Informatique'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'etudiant'
        if commit:
            user.save()
            # Créer le profil étudiant
            ProfilEtudiant.objects.create(
                user=user,
                niveau=self.cleaned_data['niveau'],
                specialite=self.cleaned_data['specialite']
            )
        return user


class InscriptionEntrepriseForm(UserCreationForm):
    """
    Formulaire d'inscription pour les entreprises
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Prénom du contact",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nom du contact",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    email = forms.EmailField(
        required=True,
        label="Email professionnel",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@entreprise.com'})
    )
    telephone = forms.CharField(
        max_length=15,
        required=True,
        label="Téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0512345678'})
    )
    nom_entreprise = forms.CharField(
        max_length=200,
        required=True,
        label="Nom de l'entreprise",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre Entreprise SA'})
    )
    secteur = forms.CharField(
        max_length=100,
        required=True,
        label="Secteur d'activité",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Informatique'})
    )
    adresse = forms.CharField(
        required=True,
        label="Adresse complète",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse de l\'entreprise'})
    )
    site_web = forms.URLField(
        required=False,
        label="Site web",
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.exemple.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'entreprise'
        if commit:
            user.save()
            # Créer le profil entreprise
            ProfilEntreprise.objects.create(
                user=user,
                nom_entreprise=self.cleaned_data['nom_entreprise'],
                secteur=self.cleaned_data['secteur'],
                adresse=self.cleaned_data['adresse'],
                site_web=self.cleaned_data.get('site_web', '')
            )
        return user


class ConnexionForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )