
# Progamação Web- Sistema De Consultas Médicas

![Sistema de Agendamento de Consultas Médicas](https://github.com/izaramos/SistemaConsultasMedicas/blob/main/consultorio/staticfiles/logo-consultorio.png)

## Descrição

Este repositório é destinado ao trabalho de implementação da disciplina de Programação WEB - GAC116. O projeto consiste em um sistema de agendamento de consultas médicas usando Django. Vão existir dois tipos de usuários no sistema: cliente e administrador. O Django será utilizado para criar uma tela de administração e uma tela de login para autenticação dos usuários.

## Funcionalidades

- **Cliente:**
  - Cadastro de conta
  - Login e autenticação
  - Agendamento de consultas
  - Visualização de consultas agendadas

- **Administrador:**
  - Gerenciamento de usuários
  - Gerenciamento de consultas
  - Painel administrativo

## Tecnologias Utilizadas

- Django
- Python
- HTML/CSS

## Pré-requisitos

- Python 3.6+
- Django 3.x
- SQLite (ou outro banco de dados de sua preferência)

## Como Rodar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LukeZaneh/ProgWeb-SistemaConsultasMedicas.git
   cd ProgWeb-SistemaConsultasMedicas
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv env
   source env/bin/activate  # No Windows, use `env\Scripts\activate`
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Faça as migrações do banco de dados:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário (administrador):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação:**
   Abra o navegador e vá para `http://127.0.0.1:8000/`

## Usuários cadastrados

- Para acessar o administrador do sistema, acesse:
   ```bash
   login: administrador
   senha: 12345678
   ```

- Para acessar um usuário do sistema que tenha registros de consultas, acesse:
   ```bash
   login: izabelle
   senha: 12345678
   ```

## Equipe

- **Izabelle Ramos Tomé**
- **Lucas Carvalho**