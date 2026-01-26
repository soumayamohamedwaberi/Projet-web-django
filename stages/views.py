from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import csv

from .models import OffreStage, Candidature
from .forms import CandidatureForm, StudentRegistrationForm, CompanyRegistrationForm

# --- PAGE D'ACCUEIL ---
def accueil(request):
    return render(request, 'stages/index.html')

# --- PAGE DE CHOIX (NOUVEAU) ---
def choix_inscription(request):
    return render(request, 'stages/choix_inscription.html')

# --- INSCRIPTIONS ---
def inscription_etudiant(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Compte étudiant créé !")
            return redirect('liste_offres')
    else:
        form = StudentRegistrationForm()
    return render(request, 'stages/inscription_etudiant.html', {'form': form})

def inscription_entreprise(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Compte entreprise créé !")
            return redirect('liste_offres') # Ou un dashboard entreprise
    else:
        form = CompanyRegistrationForm()
    return render(request, 'stages/inscription_entreprise.html', {'form': form})

# --- OFFRES & CANDIDATURES ---
def liste_offres(request):
    offres = OffreStage.objects.all().order_by('-date_publication')
    return render(request, 'stages/dashboard.html', {'offres': offres})

@login_required
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    if Candidature.objects.filter(etudiant=request.user, offre=offre).exists():
        messages.warning(request, "Déjà postulé !")
        return redirect('mes_candidatures')

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            cand = form.save(commit=False)
            cand.etudiant = request.user
            cand.offre = offre
            cand.save()
            messages.success(request, "Candidature envoyée !")
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm()
    return render(request, 'stages/postuler.html', {'form': form, 'offre': offre})

@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(etudiant=request.user).order_by('-date_candidature')
    return render(request, 'stages/mes_candidatures.html', {'candidatures': candidatures})

@login_required
@require_POST
def supprimer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)
    if candidature.statut == 'en_attente':
        candidature.delete()
        messages.success(request, "Candidature supprimée.")
    else:
        messages.error(request, "Impossible de supprimer.")
    return redirect('mes_candidatures')

@login_required
def export_candidatures_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mes_candidatures.csv"'
    writer = csv.writer(response)
    writer.writerow(['Offre', 'Entreprise', 'Date', 'Statut'])
    for c in Candidature.objects.filter(etudiant=request.user):
        writer.writerow([c.offre.titre, c.offre.entreprise, c.date_candidature, c.statut])
    return response

@login_required
def dispatch_login(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    return redirect('liste_offres')