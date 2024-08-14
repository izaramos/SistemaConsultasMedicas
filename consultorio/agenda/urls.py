from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('horarios', views.horarios, name='horarios'),
    path('medicos', views.medicos, name='medicos'),
    path('medicos/detalhes/<int:id>/', views.medico_detalhes, name='detalhes_medico'),
    path('cadastrar-medico/', views.cadastrar_medico, name='cadastrar_medico'),
    path('editar-medico/<int:id>/', views.editar_medico, name='editar_medico'),
    path('excluir-medico/<int:id>/', views.excluir_medico, name='excluir_medico'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/cadastro/', views.cadastro_view, name='cadastro'),
    path('cadastrar-consulta/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('editar-consulta/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('excluir-horario/<int:horario_id>/', views.excluir_horario, name='excluir_horario'),
]