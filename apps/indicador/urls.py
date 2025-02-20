from django.urls import path
from .views import frontoffice_nps, pesquisar_interacoes, upload_view

urlpatterns = [
    path('teste',frontoffice_nps.as_view(), name='frontoffice_nps'),
    path('pesquisar_interacoes/',pesquisar_interacoes, name='pesquisar_interacoes'),
    path('upload_view',upload_view,name='upload_view')

]