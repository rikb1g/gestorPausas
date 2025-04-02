from django.urls import path
from .views import DarkHekaList, CreateDarkHeka, DarkhekaDetail, UpdateView, delete_darkheka, DarkhekaUpdate

urlpatterns = [
    path('darkhekamain',DarkHekaList.as_view(),name="dark_heka_list"),
    path('novo_darkheka',CreateDarkHeka.as_view(),name="novo_darkheka"),
    path('details_darkheka/<int:pk>/',DarkhekaDetail.as_view(),name="details_darkheka"),
    path('editar_darkheka/<int:pk>/',DarkhekaUpdate.as_view(),name="editar_darkheka"),
    path('delete_darkheka/<int:pk>/',delete_darkheka,name="delete_darkheka"),
]

