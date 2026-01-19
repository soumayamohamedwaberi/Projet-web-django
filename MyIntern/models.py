
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec les types
     """
    USER_TYPES = (
    ('etudiant', 'Etudiant'),
    ('entrepise', 'Entrepise'),
    ('admin','Administrateur'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        verbose_name="type d'utilisateur",
    )
    telephone =models.CharField(
        max_length=15,
        blank=True,
        verbose_name="telephone",
    )
    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

class ProfilEtudiant(models.Model):
    """
    Profil spécifique pour les etudiants
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_etudiants'
    )
    niveau = models.CharField(
        max_length=50,
        verbose_name="Niveau d'études",
        help_text="EX: 2ème année cycle ingénieur"
    )
    specialiste = models.CharField(
        max_length=100,
        verbose_name="Spécialiste",
    )
    cv = models.FileField(
         upload_to="cv/",
        blank=True,
        null=True,
        verbose_name='CV (PDF)'
    )
    date_naissance =models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de naissance"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Biographie",
        help_text="Quelques lignes sur vous"
    )
    class Meta:
     verbose_name = "Profil Etudiant"
     verbose_name_plural = "Profils Etudiants"
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialiste}"

class ProfilEntreprise(models.Model):
    """
    Profil spécifique pour les entreprises
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil_entrepise'
    )
    nom_entreprise = models.CharField(
        max_length=200,
        verbose_name="Nom de l'entreprise",

    )
    secteur = models.CharField(
        max_length=100,
        verbose_name="Secteur d'activité",
        help_text="Ex: Informatique, Finace, Santé..."

    )
    adresse = models.TextField(
        verbose_name="Adresse complète",
    )
    site_web = models.URLField(
        blank=True,
        verbose_name="Site web",
    )
    logo = models.ImageField(
        upload_to='logos/',
        blank=True,
        null=True,
        verbose_name="Logo de l'entreprise",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description de l'entreprise",

    )
    class Meta:
        verbose_name = "Profil Entreprise"
        verbose_name_plural = "Profils Entreprises"
    def __str__(self):
        return self.nom_entreprise