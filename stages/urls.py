from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil (Racine)
    path('', views.accueil, name='accueil'),

    # La page de choix (Celle de la vidéo avec les deux cartes)
    path('inscription/', views.choix_inscription, name='choix_inscription'),

    # Les formulaires spécifiques
    path('inscription/etudiant/', views.inscription_etudiant, name='inscription_etudiant'),
    path('inscription/entreprise/', views.inscription_entreprise, name='inscription_entreprise'),

    # Les offres et le reste
    path('offres/', views.liste_offres, name='liste_offres'),
    path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('mes-candidatures/csv/', views.export_candidatures_csv, name='export_candidatures_csv'),
    path('supprimer/<int:candidature_id>/', views.supprimer_candidature, name='supprimer_candidature'),
    path('redirect-login/', views.dispatch_login, name='dispatch_login'),
]