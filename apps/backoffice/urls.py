from django.urls import path
from .views import pedir_bo,iniciar_bo, finalizar_bo, cancelar_bo, maximo_bo_autorizados, cancelar_bo_supervisor



urlpatterns = [
    path('bo',pedir_bo,name="pedir_bo"),
    path('iniciar_bo',iniciar_bo,name="iniciar_bo"),
    path('finalizar_bo',finalizar_bo,name="finalizar_bo"),
    path('cancelar_bo',cancelar_bo,name="cancelar_bo"),
    path('maximo_bo_autorizados',maximo_bo_autorizados,name="maximo_bo_autorizados"),
    path('cancelar_bo_supervisor',cancelar_bo_supervisor,name="cancelar_bo_supervisor"),
]