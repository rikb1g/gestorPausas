from django.urls import path
from django.views.generic import TemplateView
from .views import iniciarIntervalo, pedir_pausa,Lista_Pausas, finalizarIntervalo, cancelar_intervalo,maximo_intervalos

urlpatterns = [
    path('pausa', pedir_pausa, name='nova_pausa'),
    path('listaIntervalos',Lista_Pausas.as_view(), name='lista_intervalos'),
    path('novo_intervalo',iniciarIntervalo, name='iniciar_intervalo'),
    path('finalizar_intervalo', finalizarIntervalo, name='finalizar_intervalo'),
    path('cancelar_intervalo', cancelar_intervalo, name='cancelar_intervalo'),
    path('maximo_intervalos', maximo_intervalos, name='maximo_intervalos'),
]