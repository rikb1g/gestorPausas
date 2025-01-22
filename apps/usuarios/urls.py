from django.urls import path
from .views import turno_funcionario

urlpatterns = [
    path('turno_funcionario/',turno_funcionario, name='turno_funcionario'),
]