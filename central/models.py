from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Cuidador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.SET_NULL, null=True)
    pressao_sistolica = models.IntegerField(null=True, blank=True)
    pressao_diastolica = models.IntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacao_o2 = models.IntegerField(null=True, blank=True)
    glicemia = models.IntegerField(null=True, blank=True)
    obs =models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.paciente.nome} - {self.data_avaliacao}"


class Turno(models.Model):
    CUIDADOR_CHOICES = [
        ('CUIDADOR_1', 'Cuidador 1'),
        ('CUIDADOR_2', 'Cuidador 2'),
        # Adicione outras opções de cuidadores conforme necessário
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente')
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE, related_name='cuidador')
    turno_duracao = models.IntegerField(choices=[(24, '24 horas'), (48, '48 horas'), (72, '72 horas')])
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    
    
    def natural_key(self):
        return {
            'paciente_nome': self.paciente.nome,
            'cuidador': self.cuidador,
            'turno_duracao': self.turno_duracao,
            'data_inicio': self.data_inicio.isoformat(),
            'data_fim': self.data_fim.isoformat()
        }
    def __str__(self):
        return f"Turno de {self.cuidador} para {self.paciente.nome} - {self.data_inicio} a {self.data_fim}"
