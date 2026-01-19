from django.db import models
from django.contrib.auth.models import User

class OffreStage(models.Model):
    titre = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200)
    description = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} chez {self.entreprise}"

class Candidature(models.Model):
    # ⚠️ IMPORTANT : Cette liste doit être définie AVANT les champs en dessous
    STATUT_CHOIX = [
        ('en_attente', '⏳ En attente'),
        ('accepte', '✅ Accepté'),
        ('refuse', '❌ Refusé'),
    ]

    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE)
    lettre_motivation = models.TextField()
    cv_personnalise = models.FileField(upload_to='cvs/', null=True, blank=True)
    date_candidature = models.DateTimeField(auto_now_add=True)
    
    # Maintenant que la liste existe au-dessus, on peut l'utiliser ici 👇
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en_attente')

    def __str__(self):
        return f"Candidature de {self.etudiant.username} pour {self.offre.titre}"