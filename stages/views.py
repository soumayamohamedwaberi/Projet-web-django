from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OffreStage, Candidature
from .forms import CandidatureForm
from .forms import OffreStageForm

# vues CRUD offres
def liste_offres(request):
    offres = OffreStage.objects.filter(est_active=True)
    return render(request, 'stages/liste_offres.html', {'offres': offres})

def detail_offre(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)
    return render(request, 'stages/detail_offre.html', {'offre': offre})

@login_required
def creer_offre(request):
    if request.user.user_type != 'entreprise':
        messages.error(request, "Accès refusé.")
        return redirect('liste_offres')

    if request.method == 'POST':
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = request.user.profilentreprise
            offre.save()
            messages.success(request, "Offre créée avec succès.")
            return redirect('liste_offres')
    else:
        form = OffreStageForm()

    return render(request, 'stages/creer_offre.html', {'form': form})

@login_required
def modifier_offre(request, pk):
    offre = get_object_or_404(
        OffreStage,
        pk=pk,
        entreprise=request.user.profilentreprise
    )

    if request.method == 'POST':
        form = OffreStageForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre modifiée.")
            return redirect('liste_offres')
    else:
        form = OffreStageForm(instance=offre)

    return render(
        request,
        'stages/modifier_offre.html',
        {'form': form, 'offre': offre}
    )








# Page 1 : Liste temporaire des offres (pour tester)
def liste_offres(request):
    offres = OffreStage.objects.all()
    return render(request, 'stages/liste.html', {'offres': offres})

# Page 2 : L'action de postuler (Ton coeur de métier)
@login_required(login_url='/admin/') # Redirige vers l'admin si pas connecté
def postuler(request, offre_id):
    offre = get_object_or_404(OffreStage, id=offre_id)
    
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm()
    
    return render(request, 'stages/postuler.html', {'form': form, 'offre': offre})

# Page 3 : Le tableau de bord étudiant
@login_required(login_url='/admin/')
def mes_candidatures(request):
    mes_candidatures = Candidature.objects.filter(etudiant=request.user)
    return render(request, 'stages/dashboard.html', {'candidatures': mes_candidatures})
