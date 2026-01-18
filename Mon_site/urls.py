"""
URL configuration for Mon_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


#Vue temporaire pour la page d'accueil
def home(request):
    return render(request,'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('stages/', include('stages.urls')),
    path('', include('stages.urls')),
=======
    path('',home,name= 'home'),
    path('MyIntern/', include('MyIntern.urls')),

>>>>>>> 02b0d78af50005b66f217e09c16bf9cc122eff48
]

#Servir les fichiers média en developpement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)