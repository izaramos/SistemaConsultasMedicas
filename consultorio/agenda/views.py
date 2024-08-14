import os
import json
import locale
from datetime import datetime, time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MedicoForm, ConsultaForm, EditarConsultaForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
from django.utils.dateparse import parse_date

def principal(request):
    return render(request, 'principal.html')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_normal_user(user):
    return not user.is_staff

# DEFS DE LOGIN ----------------------------------------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('principal')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso')
            return redirect('login')
    return render(request, 'cadastro.html')

# DEFS DE CONSULTA ---------------------------------------------------------------------------------------
def carregar_horarios():
    filename = os.path.join(BASE_DIR, 'agenda', 'horarios.json')
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    else:
        print("Arquivo não encontrado:", filename)
    return []

def horarios(request):
    context = {
        'horarios': carregar_horarios()
    }
    return render(request, 'horarios.html', context)

def salvar_consulta(consulta):
    filename = os.path.join(os.path.dirname(__file__), 'horarios.json')
    horarios = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            horarios = json.load(file)
    if horarios:
        ultimo_id = max(horario['id'] for horario in horarios)
    else:
        ultimo_id = 0
    consulta['id'] = ultimo_id + 1
    horarios.append(consulta)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(horarios, file, ensure_ascii=False, indent=4)

@user_passes_test(is_admin)
def cadastrar_consulta(request):
    medicos = carregar_medicos()
    medicos_choices = [(medico['id'], medico['nome']) for medico in medicos]
    if request.method == 'POST':
        form = ConsultaForm(request.POST, medicos_choices=medicos_choices)
        if form.is_valid():
            medico_id = form.cleaned_data['medico']
            medico_nome = next((medico['nome'] for medico in medicos if medico['id'] == int(medico_id)), None)
            consulta = {
                'medico': medico_nome,
                'dia': form.cleaned_data['dia'].strftime('%d de %B de %Y'),
                'horario': form.cleaned_data['horario'],
            }
            salvar_consulta(consulta)
            return redirect('horarios')
    else:
        form = ConsultaForm(medicos_choices=medicos_choices)
    return render(request, 'cadastrar_consulta.html', {'form': form})

def salvar_horarios(horarios):
    for horario in horarios:
        if isinstance(horario['horario'], time):
            horario['horario'] = horario['horario'].strftime('%H:%M')
    with open('agenda/horarios.json', 'w', encoding='utf-8') as file:
        json.dump(horarios, file, indent=4, ensure_ascii=False)

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')  # Linux/Mac
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')  # Windows

@user_passes_test(is_admin)
def editar_consulta(request, consulta_id):
    horarios = carregar_horarios()
    consulta = next((h for h in horarios if h['id'] == consulta_id), None)
    if not consulta:
        return HttpResponse("Consulta não encontrada", status=404)
    if request.method == 'POST':
        form = EditarConsultaForm(request.POST)
        if form.is_valid():
            consulta['dia'] = form.cleaned_data['dia'].strftime('%d de %B de %Y')
            consulta['horario'] = form.cleaned_data['horario'].strftime('%H:%M')
            salvar_horarios(horarios)
            return redirect('horarios')
    else:
        dia_str = consulta['dia']
        dia_formatado = datetime.strptime(dia_str, '%d de %B de %Y').date()
        horario_formatado = datetime.strptime(consulta['horario'], '%H:%M').time()

        form = EditarConsultaForm(initial={
            'dia': dia_formatado,
            'horario': horario_formatado
        })
    return render(request, 'editar_consulta.html', {
        'form': form,
        'medico': consulta['medico'] 
    })

@user_passes_test(is_admin)
def excluir_horario(request, horario_id):
    horarios = carregar_horarios()
    horarios = [h for h in horarios if h['id'] != horario_id]
    salvar_horarios(horarios)
    return redirect('horarios')

class PeriodoForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Data de Início")
    data_fim = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Data de Fim")

@user_passes_test(is_admin)
def consultas_marcadas(request):
    consultas_filtradas = []
    data_inicio = None
    data_fim = None
    if request.method == 'POST':
        data_inicio_str = request.POST.get('data_inicio')
        data_fim_str = request.POST.get('data_fim')
        if data_inicio_str:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        if data_fim_str:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        if data_inicio and data_fim:
            for usuario in User.objects.all():
                filename = os.path.join(BASE_DIR, 'agenda', f'{usuario.username}_consultas.json')
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        consultas = json.load(f)
                        for consulta in consultas:
                            try:
                                # Converter a string de data da consulta para um objeto date
                                data_consulta = datetime.strptime(consulta.get('dia', ''), '%d de %B de %Y').date()
                            except ValueError:
                                data_consulta = None

                            # Verificar se a data da consulta está dentro do intervalo
                            if data_consulta and data_inicio <= data_consulta <= data_fim:
                                consultas_filtradas.append({
                                    'medico': consulta['medico'],
                                    'dia': consulta['dia'],
                                    'horario': consulta['horario'],
                                    'paciente': usuario.username
                                })

    context = {
        'consultas_filtradas': consultas_filtradas
    }
    return render(request, 'consultas_marcadas.html', context)

@login_required
def marcar_consulta(request, horario_id):
    horarios = carregar_horarios()
    horario_selecionado = next((h for h in horarios if h['id'] == horario_id), None)
    if horario_selecionado:
        horarios.remove(horario_selecionado)
        salvar_horarios(horarios)
        adicionar_consulta_usuario(request.user, horario_selecionado)
        return redirect('minhas_consultas')
    return redirect('horarios')

def adicionar_consulta_usuario(usuario, horario):
    filename = os.path.join(BASE_DIR, 'agenda', f'{usuario.username}_consultas.json')
    consultas = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
    consultas.append(horario)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(consultas, f, indent=4, ensure_ascii=False)

@login_required
def minhas_consultas(request):
    filename = os.path.join(BASE_DIR, 'agenda', f'{request.user.username}_consultas.json')
    consultas = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
    return render(request, 'minhas_consultas.html', {'consultas': consultas})

@login_required
def desmarcar_consulta(request, consulta_id):
    filename = os.path.join(BASE_DIR, 'agenda', f'{request.user.username}_consultas.json')
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
        consulta_selecionada = next((c for c in consultas if c['id'] == consulta_id), None)
        if consulta_selecionada:
            consultas.remove(consulta_selecionada)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(consultas, f, indent=4, ensure_ascii=False)

            # Re-adiciona a consulta em horarios.json
            horarios = carregar_horarios()
            horarios.append(consulta_selecionada)
            salvar_horarios(horarios)
    return redirect('minhas_consultas')

# DEFS DE MÉDICOS ---------------------------------------------------------------------------------------------------
def carregar_medicos():
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'medicos.json')
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        return json.load(file)

def medicos(request):
    medicos = carregar_medicos()
    return render(request, 'medicos.html', {'medicos': medicos})

def medico_detalhes(request, id):
    medicos = carregar_medicos()
    medico = next((m for m in medicos if m["id"] == id), None)
    if medico is None:
        return HttpResponse("Médico não encontrado", status=404)
    return render(request, 'medico_detalhes.html', {'medico': medico})

def salvar_medico(data):
    filename = os.path.join(BASE_DIR, 'agenda', 'medicos.json')
    if os.path.exists(filename):
        with open(filename, 'r+', encoding='utf-8') as f:
            medicos = json.load(f)
            medicos.append(data)
            f.seek(0)
            json.dump(medicos, f, indent=4)
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([data], f, indent=4)

@user_passes_test(is_admin)
def cadastrar_medico(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        planos = request.POST.get('planos')
        preco = request.POST.get('preco')

        novo_medico = {
            "id": len(carregar_medicos()) + 1,
            "nome": nome,
            "especialidade": especialidade,
            "planos": planos,
            "preco": preco
        }
        salvar_medico(novo_medico)
        return redirect('medicos')
    return render(request, 'cadastrar_medico.html')

def salvar_todos_medicos(medicos):
    filename = os.path.join(BASE_DIR, 'agenda', 'medicos.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(medicos, f, indent=4)

@user_passes_test(is_admin)
def editar_medico(request, id):
    medicos = carregar_medicos()
    medico = next((m for m in medicos if m['id'] == id), None)
    if not medico:
        return render(request, 'medico_nao_encontrado.html')
    if request.method == 'POST':
        medico['preco'] = request.POST.get('preco')
        salvar_todos_medicos(medicos)
        return redirect('medicos')
    context = {
        'medico': medico
    }
    return render(request, 'editar_medico.html', context)

@user_passes_test(is_admin)
def excluir_medico(request, id):
    medicos = carregar_medicos()
    medicos = [m for m in medicos if m["id"] != id]
    caminho_arquivo = os.path.join(BASE_DIR, 'agenda', 'medicos.json')
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        json.dump(medicos, file, indent=4, ensure_ascii=False)
        
    return redirect('medicos')