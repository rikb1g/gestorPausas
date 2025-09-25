from django.urls import path
from .views import (iniciar_intervalo, pedir_pausa, finalizar_intervalo,Lista_Pausas ,cancelar_intervalo,maximo_intervalos,
                     autorizar_intervalo,calcular_tempo_pausa,verificar_estado_pedidos_pausa_e_bo)

urlpatterns = [
    path('pedir_pausa/',pedir_pausa, name='nova_pausa'),
    path('listaIntervalos/',Lista_Pausas.as_view(), name='lista_intervalos'),
    path('iniciarIntervalo/',iniciar_intervalo, name='iniciar_intervalo'),
    path('finalizar_intervalo/', finalizar_intervalo, name='finalizar_intervalo'),
    path('cancelar_intervalo/', cancelar_intervalo, name='cancelar_intervalo'),
    path('maximo_intervalos/<str:teve_intervalo>/', maximo_intervalos, name='maximo_intervalos_intervalos'),
    path('autorizar_intervalo/', autorizar_intervalo, name='autorizar_intervalo'),
    path('calcular_tempo_pausa/<int:id>/', calcular_tempo_pausa, name='calcular_tempo_pausa'),
    path('verificar_estado_pedidos_pausa_e_bo/',verificar_estado_pedidos_pausa_e_bo, name='consultas_estados'),
]

