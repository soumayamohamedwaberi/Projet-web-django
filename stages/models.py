from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modèle pour les offres de stage
class OffreStage(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    entreprise = models.CharField(max_length=200)
    date_publication = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

# Modèle pour les candidatures
class Candidature(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE)
    date_candidature = models.DateTimeField(auto_now_add=True)
    
    # 👇 C'EST CE CHAMP QUI MANQUAIT !
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    
    lettre_motivation = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"{self.etudiant.username} - {self.offre.titre}"