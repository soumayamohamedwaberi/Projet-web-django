from django.urls import path
from . import views

urlpatterns = [
    # Partie Commune (Liste et Détail)
    path('', views.liste_offres, name='liste_offres'),
    path('<int:pk>/', views.detail_offre, name='detail_offre'),

    # Ta partie (Candidatures)
    path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('supprimer/<int:candidature_id>/', views.supprimer_candidature, name='supprimer_candidature'),
    path('export-csv/', views.export_candidatures_csv, name='export_candidatures_csv'),

    # La partie de tes collègues (Gestion des offres)
    path('creer/', views.creer_offre, name='creer_offre'),
    path('<int:pk>/modifier/', views.modifier_offre, name='modifier_offre'),
]