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
    path('entreprise/dashboard/', views.dashboard_entreprise, name='dashboard_entreprise'),
    path('offre/creer/', views.creer_offre, name='creer_offre'),
    # ... tes autres lignes ...
    path('offre/voir/<int:offre_id>/', views.voir_offre, name='voir_offre'),
    path('offre/supprimer/<int:offre_id>/', views.supprimer_offre, name='supprimer_offre'),
    # ... autres urls ...
    path('candidature/accepter/<int:candidature_id>/', views.accepter_candidature, name='accepter_candidature'),
    path('candidature/refuser/<int:candidature_id>/', views.refuser_candidature, name='refuser_candidature'),

]