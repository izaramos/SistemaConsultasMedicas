from django.db import models
from django.contrib.auth.models import User

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    planos = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.CharField(max_length=100)
    dia = models.DateField()
    horario = models.TimeField()

    def __str__(self):
        return f"{self.paciente} - {self.medico.nome} ({self.dia} {self.horario})"

class MarcarConsulta(models.Model):
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    paciente = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()

    def __str__(self):
        return f"{self.paciente} - {self.medico.nome} ({self.data} {self.horario})"