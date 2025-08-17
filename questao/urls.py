from django.urls import path
from . import views

urlpatterns = [
    path('questao/<int:pk>/', views.visualizar_questao, name='visualizar_questao'),
    path('get-assuntos/<int:materia_id>/', views.get_assuntos, name='get_assuntos'),    
]