from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(include('apps.core.urls'))),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('pausas/',include('apps.pausas.urls')),
    path('home/',include('apps.core.urls')),
    path('backoffice/',include('apps.backoffice.urls')),
]
