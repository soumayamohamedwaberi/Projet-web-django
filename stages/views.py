import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OffreStage, Candidature
# J'ai combiné les imports de formulaires ici :
from .forms import CandidatureForm, OffreStageForm

# ---------------------------------------------------------
# PARTIE COMMUNE (Lecture des offres)
# ---------------------------------------------------------

def liste_offres(request):
    # J'utilise la version simple qui marche avec ton template liste.html
    offres = OffreStage.objects.all()
    return render(request, 'stages/liste.html', {'offres': offres})

def detail_offre(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)
    # Attention: Tes collègues utilisent peut-être 'detail_offre.html'
    # Si ça plante, vérifie si ce fichier existe.
    return render(request, 'stages/detail_offre.html', {'offre': offre})

# ---------------------------------------------------------
# TA PARTIE (Candidatures Étudiants)
# ---------------------------------------------------------

@login_required(login_url='/admin/')
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()
            messages.success(request, "Ta candidature a bien été envoyée !")
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm()
    
    return render(request, 'stages/postuler.html', {'form': form, 'offre': offre})

@login_required(login_url='/admin/')
def mes_candidatures(request):
    # Utilise le template que tu as créé (mes_candidatures.html)
    mes_candidatures = Candidature.objects.filter(etudiant=request.user)
    return render(request, 'stages/mes_candidatures.html', {'candidatures': mes_candidatures})

@login_required
def supprimer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)
    
    if request.method == 'POST':
        if candidature.statut == 'en_attente':
            candidature.delete()
            messages.success(request, "Candidature retirée avec succès.")
        else:
            messages.error(request, "Impossible de supprimer une candidature déjà traitée.")
            
    return redirect('mes_candidatures')

@login_required
def export_candidatures_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mes_candidatures.csv"'

    writer = csv.writer(response)
    writer.writerow(['Offre de stage', 'Entreprise', 'Date candidature', 'Statut', 'Lettre Motivation'])

    candidatures = Candidature.objects.filter(etudiant=request.user)

    for c in candidatures:
        writer.writerow([
            c.offre.titre,
            c.offre.entreprise,
            c.date_candidature.strftime("%d/%m/%Y"),
            c.get_statut_display(),
            c.lettre_motivation[:100]
        ])

    return response

# ---------------------------------------------------------
# PARTIE COLLEGUES (Gestion Entreprise)
# ---------------------------------------------------------

@login_required
def creer_offre(request):
    # Vérification basique (à adapter selon votre modèle User)
    if hasattr(request.user, 'user_type') and request.user.user_type != 'entreprise':
        messages.error(request, "Accès refusé.")
        return redirect('liste_offres')

    if request.method == 'POST':
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            # Attention: Si tu n'as pas encore de profil entreprise, cette ligne peut planter
            if hasattr(request.user, 'profilentreprise'):
                offre.entreprise = request.user.profilentreprise
            offre.save()
            messages.success(request, "Offre créée avec succès.")
            return redirect('liste_offres')
    else:
        form = OffreStageForm()

    return render(request, 'stages/creer_offre.html', {'form': form})

@login_required
def modifier_offre(request, pk):
    # On récupère l'offre seulement si elle appartient à l'entreprise connectée
    # Note: J'ai simplifié le filtre pour éviter les erreurs si tu n'as pas 'profilentreprise'
    offre = get_object_or_404(OffreStage, pk=pk)

    if request.method == 'POST':
        form = OffreStageForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre modifiée.")
            return redirect('liste_offres')
    else:
        form = OffreStageForm(instance=offre)

    return render(request, 'stages/modifier_offre.html', {'form': form, 'offre': offre})