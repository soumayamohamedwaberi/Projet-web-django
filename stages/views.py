from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import csv
from .models import OffreStage, Candidature
from .forms import CandidatureForm

# 1. Page d'accueil : Affiche la liste des offres (Cartes)
def liste_offres(request):
    offres = OffreStage.objects.all().order_by('-date_publication')
    # On utilise 'dashboard.html' car c'est là qu'on va mettre le design des cartes
    return render(request, 'stages/dashboard.html', {'offres': offres})

# 2. Page pour postuler
@login_required
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    # Vérifier si déjà postulé
    if Candidature.objects.filter(etudiant=request.user, offre=offre).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre !")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()
            messages.success(request, "Candidature envoyée avec succès ! 🚀")
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm()

    return render(request, 'stages/postuler.html', {'form': form, 'offre': offre})

# 3. Page "Mes Candidatures"
@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(etudiant=request.user).order_by('-date_candidature')
    return render(request, 'stages/mes_candidatures.html', {'candidatures': candidatures})

# 4. Suppression d'une candidature
@login_required
@require_POST
def supprimer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)
    if candidature.statut == 'en_attente':
        candidature.delete()
        messages.success(request, "Candidature retirée.")
    else:
        messages.error(request, "Impossible de supprimer une candidature déjà traitée.")
    return redirect('mes_candidatures')

# 5. Export CSV
@login_required
def export_candidatures_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mes_candidatures.csv"'
    writer = csv.writer(response)
    writer.writerow(['Offre', 'Entreprise', 'Date', 'Statut'])
    candidatures = Candidature.objects.filter(etudiant=request.user)
    for c in candidatures:
        writer.writerow([c.offre.titre, c.offre.entreprise, c.date_candidature, c.statut])
    return response
# stages/views.py

@login_required
def dispatch_login(request):
    # Si l'utilisateur est un SuperUser ou un membre du Staff (Admin)
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')  # 👉 Direction le panneau Admin
    
    # Sinon, c'est un étudiant normal
    return redirect('liste_offres')  # 👉 Direction les offres de stage