from django.urls import path
from apps.iqs import views

from . import views

urlpatterns = [
    path('listar_iqs/', views.IqsListView.as_view(), name='listar_iqs'),
    path('novo_iqs_fo/', views.iqs_front_office_submit, name='iqs'),
    path('novo_iqs_bo/', views.iqs_back_office_submit, name='iqs'),
    path('anular_iqs_fo/', views.eliminar_iqs_fo, name='eliminar_iqs'),
    path('anular_iqs_bo/', views.eliminar_iqs_bo, name='eliminar_iqs'),
]