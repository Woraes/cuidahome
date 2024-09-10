from django.urls import path
from . import views

urlpatterns = [
    # Pacientes
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/criar/', views.criar_paciente, name='criar_paciente'),
    path('pacientes/editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    
    #Cuidadores
    path('cuidadores/', views.listar_cuidadores, name='listar_cuidadores'),
    path('cuidadores/criar/', views.criar_cuidador, name='criar_cuidador'),
    path('cuidadores/editar/<int:cuidador_id>/', views.editar_cuidador, name='editar_cuidador'),


    # Avaliações
    path('avaliacoes/criar/', views.criar_avaliacao, name='criar_avaliacao'),

    # Turnos
    path('turnos/', views.listar_turnos, name='listar_turnos'),
    path('turnos/criar/', views.criar_turno, name='criar_turno'),
    path('turnos/editar/<int:turno_id>/', views.editar_turno, name='editar_turno'),
    
    #home
    path('', views.home, name='home'),
    #Login
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),  # Adicione esta linha
  

]

