from django.db import models
from django.contrib.auth.models import User 

# 1. Version simplifiée de l'Offre
class OffreStage(models.Model):
    titre = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200, default="Entreprise Test")
    description = models.TextField()
    
    def __str__(self):
        return self.titre

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