
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include('apps.core.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('pausa',include('apps.pausas.urls')),
]
