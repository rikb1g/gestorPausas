from django.urls import path
from .views import *



urlpatterns = [
    path('bo',pedir_bo,name="pedir_bo"),
    path('iniciar_bo',iniciar_bo,name="iniciar_bo"),
    path('finalizar_bo',finalizar_bo,name="finalizar_bo"),
    path('cancelar_bo',cancelar_bo,name="cancelar_bo"),
    path('maximo_bo_autorizados',maximo_bo_autorizados,name="maximo_bo_autorizados"),
    path('cancelar_bo_supervisor',cancelar_bo_supervisor,name="cancelar_bo_supervisor"),
    path('autorizar_bo_supervisor',autorizar_bo_supervisor,name="autorizar_bo_supervisor"),
    path('iniciar_bo_supervisor',iniciar_bo_supervisor,name="iniciar_bo_supervisor"),
    path('pausar_bo_sup',pausar_bo_sup, name='pausar_bo_sup'),
    path('despausar_bo_sup',despausar_bo_sup, name='despausar_bo_sup'),
    path('despausar_bo/<int:id>/',despausar_bo, name='despausar_bo'),
    path('pausar_bo/<int:id>/',pausar_bo, name='pausar_bo'),
    path('tempo_bo/<int:id>/',tempo_bo, name='tempo_bo'),
]