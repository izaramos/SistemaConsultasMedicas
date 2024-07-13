from django.http import HttpResponse
from django.template import loader
from .models import marcarConsulta

def principal(request):
    template = loader.get_template('principal.html')
    return HttpResponse(template.render())

def marcarConsulta(request):
    template = loader.get_template('marcarConsulta.html')
    context = {
        'marcarConsulta': [
            {
                "medico": "Ana Catarina",
                "dia": "15 de julho de 2024",
                "horario": "9:00",
                "plano": "Unimed"
            },
            {
                "medico": "Ana Catarina",
                "dia": "15 de julho de 2024",
                "horario": "9:30",
                "plano": "Unimed"
            },
            {
                "medico": "Ana Catarina",
                "dia": "15 de julho de 2024",
                "horario": "13:00",
                "plano": "Bradesco Saúde"
            },
            {
                "medico": "Ricardo Silvano",
                "dia": "15 de julho de 2024",
                "horario": "13:00",
                "plano": "Particular"
            },
            {
                "medico": "Ricardo Silvano",
                "dia": "18 de julho de 2024",
                "horario": "14:30",
                "plano": "Unimed"
            },
            {
                "medico": "Júlia Caldas",
                "dia": "18 de julho de 2024",
                "horario": "14:00",
                "plano": "Unimed"
            },
            {
                "medico": "Júlia Caldas",
                "dia": "18 de julho de 2024",
                "horario": "15:00",
                "plano": "Unimed"
            },
            {
                "medico": "Júlia Caldas",
                "dia": "18 de julho de 2024",
                "horario": "15:30",
                "plano": "Particular"
            },
        ]
    }
    return HttpResponse(template.render(context, request))

def consultas(request):
    template = loader.get_template('consultas.html')
    context = {
        'consultas': [
            {
                "id": 1,
                "medico": "Júlia Caldas",
                "dia": "05 de janeiro de 2023",
                "horario": "08:00",
                "plano": "Unimed"
            },
            {
                "id": 2,
                "medico": "Júlia Caldas",
                "dia": "05 de julho de 2023",
                "horario": "08:30",
                "plano": "Unimed"
            },
            {
                "id": 3,
                "medico": "Júlia Caldas",
                "dia": "08 de outubro de 2023",
                "horario": "13:00",
                "plano": "Unimed"
            },
            {
                "id": 4,
                "medico": "Ricardo Silvano",
                "dia": "15 de maio de 2024",
                "horario": "15:00",
                "plano": "Unimed"
            },
            {
                "id": 5,
                "medico": "Alessandra Nunes",
                "dia": "01 de julho de 2024",
                "horario": "17:30",
                "plano": "Particular"
            }
        ]
    }
    return HttpResponse(template.render(context, request))

def consulta_detalhes(request, id): 
    consultas = [
        {
                "id": 1,
                "medico": "Júlia Caldas",
                "dia": "05 de janeiro de 2023",
                "horario": "08:00",
                "plano": "Unimed"
            },
            {
                "id": 2,
                "medico": "Júlia Caldas",
                "dia": "05 de julho de 2023",
                "horario": "08:30",
                "plano": "Unimed"
            },
            {
                "id": 3,
                "medico": "Júlia Caldas",
                "dia": "08 de outubro de 2023",
                "horario": "13:00",
                "plano": "Unimed"
            },
            {
                "id": 4,
                "medico": "Ricardo Silvano",
                "dia": "15 de maio de 2024",
                "horario": "15:00",
                "plano": "Unimed"
            },
            {
                "id": 5,
                "medico": "Alessandra Nunes",
                "dia": "01 de julho de 2024",
                "horario": "17:30",
                "plano": "Particular"
            }
    ]
    consulta = consultas[id-1]
    template = loader.get_template('consulta_detalhes.html')
    context = {
        'consulta': consulta,
    }
    return HttpResponse(template.render(context, request))