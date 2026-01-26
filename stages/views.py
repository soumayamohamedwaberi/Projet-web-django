from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import csv

from .models import OffreStage, Candidature
from .forms import CandidatureForm, StudentRegistrationForm, CompanyRegistrationForm, OffreForm

# ============================================================
# 1. ACCUEIL & CHOIX
# ============================================================
def accueil(request):
    return render(request, 'stages/index.html')

def choix_inscription(request):
    return render(request, 'stages/choix_inscription.html')

# ============================================================
# 2. INSCRIPTIONS
# ============================================================
def inscription_etudiant(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Étiquette "Etudiant"
            group, created = Group.objects.get_or_create(name='Etudiant')
            user.groups.add(group)
            
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
            
            # Étiquette "Entreprise"
            group, created = Group.objects.get_or_create(name='Entreprise')
            user.groups.add(group)
            
            login(request, user)
            messages.success(request, "Compte entreprise créé !")
            return redirect('dashboard_entreprise') 
    else:
        form = CompanyRegistrationForm()
    return render(request, 'stages/inscription_entreprise.html', {'form': form})

# ============================================================
# 3. ROUTAGE LOGIN (Aiguillage)
# ============================================================
@login_required
def dispatch_login(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    
    if request.user.groups.filter(name='Entreprise').exists():
        return redirect('dashboard_entreprise')
    
    return redirect('liste_offres')

# ============================================================
# 4. ESPACE ENTREPRISE
# ============================================================
@login_required
def dashboard_entreprise(request):
    # Sécurité : Vérifier que c'est une entreprise
    if not request.user.groups.filter(name='Entreprise').exists():
         return redirect('liste_offres')

    # Récupérer les données
    offres = OffreStage.objects.filter(entreprise=request.user.username).order_by('-date_publication')
    candidatures = Candidature.objects.filter(offre__in=offres)
    
    context = {
        'offres': offres,
        'nb_offres': offres.count(),
        'nb_candidatures': candidatures.count(),
        'nb_en_attente': candidatures.filter(statut='en_attente').count(),
    }
    return render(request, 'stages/dashboard_entreprise.html', context)

@login_required
def creer_offre(request):
    if not request.user.groups.filter(name='Entreprise').exists():
        return redirect('liste_offres')

    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = request.user.username
            offre.save()
            messages.success(request, "Offre publiée avec succès !")
            return redirect('dashboard_entreprise')
    else:
        form = OffreForm()
    
    return render(request, 'stages/creer_offre.html', {'form': form})

# ============================================================
# 5. ESPACE ÉTUDIANT (Offres & Candidatures)
# ============================================================
def liste_offres(request):
    # C'est cette fonction qui manquait !
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
# ... à la fin du fichier ...

@login_required
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    # Sécurité : On vérifie que c'est bien l'entreprise qui a créé l'offre
    if offre.entreprise != request.user.username:
        messages.error(request, "Action non autorisée.")
        return redirect('dashboard_entreprise')

    offre.delete()
    messages.success(request, "L'offre a été supprimée.")
    return redirect('dashboard_entreprise')

@login_required
def voir_offre(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    # Sécurité
    if offre.entreprise != request.user.username:
        return redirect('dashboard_entreprise')

    # On récupère les candidats pour CETTE offre
    candidatures = Candidature.objects.filter(offre=offre).order_by('-date_candidature')
    
    return render(request, 'stages/detail_offre_entreprise.html', {
        'offre': offre,
        'candidatures': candidatures
    })
# ... tout en bas du fichier ...

@login_required
def accepter_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    # Vérifie que l'entreprise est bien propriétaire de l'offre
    if candidature.offre.entreprise == request.user.username:
        candidature.statut = 'accepte'
        candidature.save()
        messages.success(request, f"Candidature de {candidature.etudiant.username} acceptée !")
    return redirect('voir_offre', offre_id=candidature.offre.id)

@login_required
def refuser_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    # Vérifie que l'entreprise est bien propriétaire de l'offre
    if candidature.offre.entreprise == request.user.username:
        candidature.statut = 'refuse'
        candidature.save()
        messages.warning(request, f"Candidature de {candidature.etudiant.username} refusée.")
    return redirect('voir_offre', offre_id=candidature.offre.id)