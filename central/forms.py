from django import forms
from .models import Paciente, Cuidador, Avaliacao, Turno
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Cuidador



class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

class CuidadorForm(forms.ModelForm):
    class Meta:
        model = Cuidador
        fields = '__all__'


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cuidador
        fields = ['nome', 'cpf', 'telefone', 'endereco', 'password']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['cpf'],
            password=self.cleaned_data['password']
        )
        cuidador = super().save(commit=False)
        cuidador.user = user
        if commit:
            cuidador.save()
        return cuidador

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['paciente', 'pressao_sistolica', 'pressao_diastolica', 'temperatura', 'saturacao_o2', 'glicemia', 'obs']

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['cuidador', 'paciente', 'data_inicio', 'data_fim', 'turno_duracao']

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        cuidador = cleaned_data.get('cuidador')

        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValidationError("A data de início não pode ser posterior à data de fim.")

        # Verificar se já existe um turno para o cuidador nas datas fornecidas
        turnos_conflitantes = Turno.objects.filter(
            cuidador=cuidador,
            data_inicio__lt=data_fim,  # Início de um turno existente antes do fim do novo turno
            data_fim__gt=data_inicio    # Fim de um turno existente após o início do novo turno
        ).exists()

        if turnos_conflitantes:
            raise ValidationError(f"O cuidador {cuidador.nome} já possui um turno nessas datas.")

        return cleaned_data     
        
