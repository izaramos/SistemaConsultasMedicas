from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('marcarConsulta', views.marcarConsulta, name='marcarConsulta'),
    path('consultas', views.consultas, name='consultas'),
    path('consultas/detalhes/<int:id>', views.consulta_detalhes, name='consulta_detalhes'),
]