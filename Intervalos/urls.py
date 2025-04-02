from django.contrib import admin
from django.urls import path, include
from apps.usuarios.views import CustomLoginView
from django.conf.urls.static import static  
from django.conf import settings


urlpatterns = [
    path('', include('apps.core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('pausas/', include('apps.pausas.urls')),
    path('home/', include('apps.core.urls')),
    path('backoffice/', include('apps.backoffice.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('indicadores/', include('apps.indicador.urls')),
    path('darkheka/', include('apps.darkheka.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
