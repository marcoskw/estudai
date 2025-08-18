from django.urls import path
from . import views

urlpatterns = [
# HOME
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Home
    path('/home', views.home, name='home'),

# SIMULADOS
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    path('historico_simulados/', views.historico_simulados, name='historico_simulados'),

# CONTA
    path('minha_conta/', views.minha_conta, name='minha_conta'),

# PROVAS
    path('listar_provas', views.listar_provas, name='listar_provas'),
    path('prova/<int:pk>/', views.detalhes_prova, name='detalhes_prova'),
]