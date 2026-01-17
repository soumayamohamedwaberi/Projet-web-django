from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_offres, name='liste_offres'),
    path('<int:pk>/', views.detail_offre, name='detail_offre'),
    path('creer/', views.creer_offre, name='creer_offre'),
    path('<int:pk>/modifier/', views.modifier_offre, name='modifier_offre'),
]

