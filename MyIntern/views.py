from django.shortcuts import render, redirect
from django.contrib.auth  import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionEtudiantForm, InscriptionEntrepriseForm, ConnexionForm
def inscription(request):
    """
    Page d'inscription avec choix du type d'ytilisateur
    """
    return render(request, 'MyIntern/choix_inscription.html')

def inscription_etudiant(request):
    """
    Inscription pour les éudiants
    """
    if request.method == 'POST':
        form = InscriptionEtudiantForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte étudiant a été créé avec succèss.")
            return redirect('dashboard')
    else:
            form =InscriptionEtudiantForm()
    return render(request,'MyIntern/register.html',{'form': form,'user_type':'Etudiant'
        })
def inscription_entreprise(request):
    """
    Inscription pour les entreprises
    """
    if request.method == 'POST':
        form = InscriptionEntrepriseForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue ! Votre compte entreprise a été créé avec succèss.")
            return redirect('dashboard')
    else:
            form = InscriptionEntrepriseForm()
    return render(request, 'MyIntern/register.html',{
            'form': form,
            'user_type':'Entreprise'
        })
def connexion(request):
    """
    Page de connexion
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = ConnexionForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password =form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} !")
                return redirect('dashboard')

    form = ConnexionForm()
    return render(request, 'MyIntern/login.html',{'form': form, })

@login_required
def deconnexion(request):
    """
    Déconnexion de l'utilisateur
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

@login_required
def dashboard(request):
    """
    Dashboard principal qui rdirige selon le type d'utilisateur
    """
    if request.user.user_type == 'etudiant':
         return redirect('dashboard_etudiant')
    elif request.user.sser_type =='entreprise':
         return redirect('dashboard_entreprise')
    else:
        return redirect('admin:index')

@login_required
def dashboard_etudiant(request):
    """
    Dashboard pour les etudiants
     """
    return render(request, 'MyIntern/dashboard_etudiant.html')

@login_required
def dashboard_entreprise(request):
    """
    Dashboard pour les entreprises
    """
    return render(request, 'MyIntern/dashboard_entreprise.html')

@login_required
def profil(request):
    """"
    Profil de l'utilisateur
    """
    return render(request, 'MyIntern/profil.html')



