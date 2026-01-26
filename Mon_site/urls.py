from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 👇 CORRECTION IMPORTANTE 1 :
    # On enlève 'stages/' et on met juste '' (vide).
    # Cela permet à ton site d'être accessible directement sur http://127.0.0.1:8000/
    path('', include('stages.urls')), 
    
    # 👇 CORRECTION IMPORTANTE 2 :
    # J'ai SUPPRIMÉ la ligne "RedirectView" qui te forçait à aller sur le login.
    
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)