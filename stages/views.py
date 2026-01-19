from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OffreStage, Candidature
from .forms import CandidatureForm
import csv
from django.http import HttpResponse

# Page d'accueil : Liste des offres
def liste_offres(request):
    offres = OffreStage.objects.all().order_by('-date_publication')
    return render(request, 'stages/liste.html', {'offres': offres})

# Page pour postuler (nécessite d'être connecté)
@login_required
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()
            return redirect('liste_offres')
    else:
        form = CandidatureForm()
    
    return render(request, 'stages/postuler.html', {'form': form, 'offre': offre})

# Page Dashboard : Mes candidatures
@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(etudiant=request.user)
    return render(request, 'stages/mes_candidatures.html', {'candidatures': candidatures})
@login_required
def export_candidatures_csv(request):
    # 1. On récupère les candidatures de l'étudiant connecté
    candidatures = Candidature.objects.filter(etudiant=request.user)
    
    # 2. On prépare le fichier CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mes_candidatures.csv"'
    
    writer = csv.writer(response)
    # 3. On écrit l'en-tête (les titres des colonnes)
    writer.writerow(['Offre', 'Entreprise', 'Date de candidature', 'Lettre de motivation'])
    
    # 4. On écrit les lignes
    for c in candidatures:
        writer.writerow([c.offre.titre, c.offre.entreprise, c.date_candidature, c.lettre_motivation])
        
    return response
# stages/views.py (Ajoute ça tout en bas)

from django.views.decorators.http import require_POST

@login_required
@require_POST  # Sécurité : on n'accepte que les requêtes POST (pas de suppression par simple lien)
def supprimer_candidature(request, candidature_id):
    # On récupère la candidature, mais SEULEMENT si elle appartient à l'utilisateur connecté
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)
    
    # On vérifie si le statut permet la suppression (optionnel, mais mieux)
    if candidature.statut == 'en_attente':
        candidature.delete()
        # On peut ajouter un message de succès ici si tu veux plus tard
    
    return redirect('mes_candidatures')