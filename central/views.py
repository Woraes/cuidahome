import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente, Cuidador, Avaliacao
from .forms import PacienteForm, CuidadorForm, AvaliacaoForm, RegistroForm, TurnoForm
from django.http import JsonResponse
from datetime import timedelta
from .models import Turno, Cuidador
from .forms import TurnoForm
from django.contrib.auth.forms import AuthenticationForm

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout


from django.shortcuts import render
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    """View para fazer logout do usuário"""
    auth_logout(request)
    return redirect('login')  # Redireciona para a página de login após o logout

def home(request):
    # Dados para o calendário
    turnos = Turno.objects.all().values('paciente__nome', 'cuidador__nome', 'turno_duracao', 'data_inicio', 'data_fim')
    for turno in turnos:
        turno['data_inicio'] = turno['data_inicio'].isoformat()
        turno['data_fim'] = turno['data_fim'].isoformat()
    turnos_json = json.dumps(list(turnos))
    
    # Dados do dashboard
    total_pacientes = Paciente.objects.count()
    cuidadores_em_servico = Cuidador.objects.count()
    escalas_pendentes = Turno.objects.count()

    # Passando tudo para o contexto
    context = {
        'turnos_json': turnos_json,
        'total_pacientes': total_pacientes,
        'cuidadores_em_servico': cuidadores_em_servico,
        'escalas_pendentes': escalas_pendentes,
    }

    return render(request, 'home.html', context)


# Listar Pacientes
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

# Criar Paciente
def criar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/criar.html', {'form': form})

# Editar Paciente
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/criar.html', {'form': form, 'paciente': paciente})



# Listar Cuidadores
def listar_cuidadores(request):
    cuidadores = Cuidador.objects.all()
    return render(request, 'cuidadores/listar.html', {'cuidadores': cuidadores})

# Criar Cuidador
def criar_cuidador(request):
    if request.method == 'POST':
        form = CuidadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cuidadores')
    else:
        form = CuidadorForm()
    return render(request, 'cuidadores/criar.html', {'form': form})

# Editar Cuidador
def editar_cuidador(request, cuidador_id):
    cuidador = get_object_or_404(Cuidador, id=cuidador_id)
    if request.method == 'POST':
        form = CuidadorForm(request.POST, instance=cuidador)
        if form.is_valid():
            form.save()
            return redirect('listar_cuidadores')
    else:
        form = CuidadorForm(instance=cuidador)
    return render(request, 'cuidadores/criar.html', {'form': form, 'cuidador': cuidador})

# Criar Avaliação
def criar_avaliacao(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cuidador = Cuidador.objects.get(user=request.user)
    if request.method == 'POST':
        # Processar o formulário de avaliação aqui
        pass
    avaliacao_form = AvaliacaoForm()
    return render(request, 'avaliacao/painel_avaliacao.html', {'form': avaliacao_form})


def criar_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
    else:
        form = TurnoForm()

    turnos_ocupados = Turno.objects.all()
    turnos_ocupados_json = json.dumps(list(turnos_ocupados.values('data_inicio', 'data_fim')), cls=DjangoJSONEncoder)

    context = {
        'form': form,
        'turnos_ocupados_json': turnos_ocupados_json,
    }
    return render(request, 'escalas/criar.html', context)

# Função para editar um turno existente
def editar_turno(request, turno_id):
    turno = Turno.objects.get(pk=turno_id)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('listar_turnos')
        else:
            erro = "Erro ao salvar o turno. Datas Ocupadas."
    else:
        form = TurnoForm(instance=turno)
        erro = None

    context = {
        'form': form,
        'erro': erro,
        'turno': turno
    }
    return render(request, 'escalas/criar.html', context)
# Listar Turnos (Escalas)
def listar_turnos(request):
    turnos = Turno.objects.all()
    return render(request, 'escalas/listar.html', {'turnos': turnos})

# Função para verificar a disponibilidade do cuidador
def verificar_disponibilidade(cuidador, data_inicio, data_fim, turno_id=None):
    # Se for uma edição, desconsiderar o turno atual
    turnos_conflitantes = Turno.objects.filter(
        cuidador=cuidador,
        data_inicio__lt=data_fim,  # Verificar se o início do novo turno é antes do fim de um turno existente
        data_fim__gt=data_inicio    # Verificar se o fim do novo turno é depois do início de um turno existente
    )

    if turno_id:
        # Excluir o turno atual da verificação em caso de edição
        turnos_conflitantes = turnos_conflitantes.exclude(id=turno_id)

    # Retornar se existe algum turno conflitante
    return not turnos_conflitantes.exists()
