from django import forms
from .models import Medico, Consulta

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'planos', 'preco']

class ConsultaForm(forms.Form):
    medico = forms.ChoiceField(choices=[], label="Médico")
    dia = forms.DateField(label="Dia", widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(max_length=100, label="Horário")

    def __init__(self, *args, **kwargs):
        medicos_choices = kwargs.pop('medicos_choices', [])
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.fields['medico'].choices = medicos_choices

class EditarConsultaForm(forms.Form):
    dia = forms.DateField(label='Data', widget=forms.SelectDateWidget())
    horario = forms.TimeField(label='Horário', widget=forms.TimeInput(format='%H:%M'))