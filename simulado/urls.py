from django.urls import path
from . import views

urlpatterns = [
    # Simulado
    path('home', views.home, name='home'),
#    path('concursos/', views.lista_concursos, name='lista_concursos'),
#    path('concursos/<int:pk>/', views.detalhes_concurso, name='detalhes_concurso'),
#    path('simulados/criar/', views.criar_simulado, name='criar_simulado'),
#    path('simulados/<int:pk>/resolver/', views.resolver_simulado, name='resolver_simulado'),
#    path('simulados/<int:pk>/resultado/', views.resultado_simulado, name='resultado_simulado'),
#    path('simulados/historico/', views.historico_simulados, name='historico_simulados'),
    
    # URLs para Autenticação
#    path('login/', views.login_view, name='login'),
#    path('logout/', views.logout_view, name='logout'),
#    path('registrar/', views.registrar_view, name='registrar'),
]