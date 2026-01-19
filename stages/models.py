from django.db import models
from django.contrib.auth.models import User

# On définit l'offre de stage
class OffreStage(models.Model):
    titre = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200)  # Simplifié pour éviter les erreurs
    description = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} chez {self.entreprise}"

# On définit la candidature
class Candidature(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE)
    lettre_motivation = models.TextField()
    cv_personnalise = models.FileField(upload_to='cvs/', null=True, blank=True)
    date_candidature = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature de {self.etudiant.username} pour {self.offre.titre}"