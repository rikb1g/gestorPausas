from django.contrib import admin
from django.urls import path, include
from apps.usuarios.views import CustomLoginView

urlpatterns = [
    path('', include('apps.core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('pausas/', include('apps.pausas.urls')),
    path('home/', include('apps.core.urls')),
    path('backoffice/', include('apps.backoffice.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
]
