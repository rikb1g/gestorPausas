from django.urls import path
from .views import (pedir_bo,iniciar_bo, finalizar_bo, cancelar_bo, maximo_bo_autorizados, autorizar_bo,
                    despausar_bo,pausar_bo, tempo_bo,maximos_autorizados
                    )



urlpatterns = [
    path('pedir_bo/',pedir_bo,name="pedir_bo"),
    path('iniciar_bo/',iniciar_bo,name="iniciar_bo"),
    path('finalizar_bo/',finalizar_bo,name="finalizar_bo"),
    path('cancelar_bo/',cancelar_bo,name="cancelar_bo"),
    path('maximo_bo_autorizados/<str:turno>/',maximo_bo_autorizados,name="maximo_bo_autorizados"),
    path('autorizar_bo/',autorizar_bo,name="autorizar_bo_supervisor"),
    path('retomar_bo/<int:id>/',despausar_bo, name='despausar_bo'),
    path('pausar_bo/<int:id>/<str:isPause>/',pausar_bo, name='pausar_bo'),
    path('tempo_bo/<int:id>/',tempo_bo, name='tempo_bo'),
    path('maximos_autorizados/',maximos_autorizados, name='maximos_autorizados'),
]