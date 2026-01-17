from django.db import models
from django.contrib.auth.models import User 

# 1. Version simplifiée de l'Offre

class OffreStage(models.Model):
    entreprise = models.ForeignKey(
        ProfilEntreprise,
        on_delete=models.CASCADE,
        related_name='offres'
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
    domaine = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    duree = models.IntegerField(help_text="Durée en mois")
    date_debut = models.DateField()
    competences_requises = models.TextField()
    remuneration = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    date_publication = models.DateTimeField(auto_now_add=True)
    date_limite_candidature = models.DateField()
    est_active = models.BooleanField(default=True)
    nombre_places = models.IntegerField(default=1)

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return f"{self.titre} - {self.entreprise.nom_entreprise}"

# 2. TON TRAVAIL : Le modèle Candidature
class Candidature(models.Model):
    STATUTS = (
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    )
    
    # Lien vers l'étudiant
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    # Lien vers l'offre
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE)
    
    lettre_motivation = models.TextField()
    
    cv_personnalise = models.FileField(upload_to='cvs/', blank=True, null=True)
    
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')

    def __str__(self):
        return f"{self.etudiant.username} - {self.offre.titre}"
