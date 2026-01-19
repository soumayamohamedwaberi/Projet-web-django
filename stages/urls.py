from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil (Liste des offres)
    path('', views.liste_offres, name='liste_offres'),
    
    # Page pour postuler
    path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
    
    # Page "Mes candidatures"
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    
    # Export CSV
    path('mes-candidatures/csv/', views.export_candidatures_csv, name='export_candidatures_csv'),
    
    # Suppression d'une candidature
    path('supprimer/<int:candidature_id>/', views.supprimer_candidature, name='supprimer_candidature'),
    path('redirect-login/', views.dispatch_login, name='dispatch_login'),
]