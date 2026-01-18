<<<<<<< HEAD
from django.contrib import admin
from .models import OffreStage, Candidature

admin.site.register(OffreStage)
admin.site.register(Candidature)
# Register your models here.
=======
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProfilEtudiant, ProfilEntreprise


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée du modèle User
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'telephone')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_type', 'telephone')
        }),
    )


@admin.register(ProfilEtudiant)
class ProfilEtudiantAdmin(admin.ModelAdmin):
    """
    Administration du modèle ProfilEtudiant
    """
    list_display = ['user', 'niveau', 'specialiste', 'date_naissance']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialiste']
    list_filter = ['niveau', 'specialiste']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ProfilEntreprise)
class ProfilEntrepriseAdmin(admin.ModelAdmin):
    """
    Administration du modèle ProfilEntreprise
    """
    list_display = ['nom_entreprise', 'user', 'secteur', 'site_web']
    search_fields = ['nom_entreprise', 'secteur', 'user__username']
    list_filter = ['secteur']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
>>>>>>> 02b0d78af50005b66f217e09c16bf9cc122eff48
