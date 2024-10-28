from django.urls import path
from .views import (iniciarIntervalo, pedir_pausa, finalizarIntervalo,Lista_Pausas ,cancelar_intervalo,maximo_intervalos,
                    cancelar_intervalo_sup, autorizar_intervalo_sup,calcular_tempo_pausa)

urlpatterns = [
    path('pausa', pedir_pausa, name='nova_pausa'),
    path('listaIntervalos',Lista_Pausas.as_view(), name='lista_intervalos'),
    path('novo_intervalo',iniciarIntervalo, name='iniciar_intervalo'),
    path('finalizar_intervalo', finalizarIntervalo, name='finalizar_intervalo'),
    path('cancelar_intervalo', cancelar_intervalo, name='cancelar_intervalo'),
    path('maximo_intervalos', maximo_intervalos, name='maximo_intervalos'),
    path('cancelar_intervalo_sup', cancelar_intervalo_sup, name='cancelar_intervalo_sup'),
    path('autorizar_intervalo_sup', autorizar_intervalo_sup, name='autorizar_intervalo_sup'),
    path('calcular_tempo_pausa/<int:id>/', calcular_tempo_pausa, name='calcular_tempo_pausa'),

]

