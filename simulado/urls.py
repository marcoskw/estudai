from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
# HOME
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # URLs de Recuperação de Senha
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),


    # Home
    path('home', views.home, name='home'),

# SIMULADOS
    path('criar_simulado/', views.criar_simulado, name='criar_simulado'),
    path('historico_simulados/', views.historico_simulados, name='historico_simulados'),
    path('iniciar_simulado/<int:pk>/', views.iniciar_simulado, name='iniciar_simulado'),
    path('finalizar_simulado/<int:pk>/', views.finalizar_simulado, name='finalizar_simulado'),
    path('resultado_simulado/<int:pk>/', views.resultado_simulado, name='resultado_simulado'),


# CONTA
    path('minha_conta/', views.minha_conta, name='minha_conta'),

# PROVAS
    path('listar_provas/', views.listar_provas, name='listar_provas'),
    path('prova/<int:pk>/', views.detalhes_prova, name='detalhes_prova'),
]