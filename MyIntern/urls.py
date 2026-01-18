# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Inscription
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/etudiant/', views.inscription_etudiant, name='inscription_etudiant'),
    path('inscription/entreprise/', views.inscription_entreprise, name='inscription_entreprise'),

    # Authentification
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
    path('dashboard/entreprise/', views.dashboard_entreprise, name='dashboard_entreprise'),

    # Profil
    path('profil/', views.profil, name='profil'),
]