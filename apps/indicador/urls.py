from django.urls import path
from .views import frontoffice_nps, pesquisar_interacoes, upload_view,editar_interlocutores, pesquisar_interlocutores
from .views import Interlocutores, InterlocutoresCreate,eliminar_interlocutores, List_interacoes

urlpatterns = [
    path('nps/',frontoffice_nps.as_view(), name='frontoffice_nps'),
    path('pesquisar_interacoes/',pesquisar_interacoes, name='pesquisar_interacoes'),
    path('upload_view',upload_view,name='upload_view'),
    path('pesquisar_interlocutores/',pesquisar_interlocutores, name='pesquisar_interlocutores'),
    path('editar_interlocutores/', editar_interlocutores, name='editar_interlocutores'),
    path('novo_interlocutor/', InterlocutoresCreate.as_view(), name='novo_interlocutor'),
    path('eliminar_interlocutores/<int:id>/', eliminar_interlocutores, name='eliminar_interlocutores'),
    path('list_interacoes/', List_interacoes.as_view(), name='list_interacoes'),

]