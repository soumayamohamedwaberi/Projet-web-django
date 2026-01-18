from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_offres, name='liste_offres'),
    path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
    path('<int:pk>/', views.detail_offre, name='detail_offre'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('creer/', views.creer_offre, name='creer_offre'),
    path('<int:pk>/modifier/', views.modifier_offre, name='modifier_offre'),
]

