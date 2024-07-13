from django.db import models

class marcarConsulta(models.Model):
    medico = models.CharField(max_length=255)
    dia = models.CharField(max_length=255)
    horario = models.CharField(max_length=255)
    plano = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.medico} - {self.dia} - {self.horario}"