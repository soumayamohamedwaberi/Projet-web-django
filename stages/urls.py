from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_offres, name='liste_offres'),
    path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('mes-candidatures/csv/', views.export_candidatures_csv, name='export_candidatures_csv'),
]