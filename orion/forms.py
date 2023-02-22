from datetime import datetime

from django import forms

from .models import CargaHoraria, Empresa, Endereco, Equipamento, Ordem_Servico


class OrdemServicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['numero_chamado'].initial = datetime.now().strftime(
            "%Y%m%d%H%M%S")
        self.fields['equipamento'].empty_label = "Selecione uma Opção"
        self.fields['empresa'].empty_label = "Selecione uma Opção"

    class Meta:
        model = Ordem_Servico
        exclude = ['status_chamado']
        # fields = '__all__'#['status', 'tipo_chamado']


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ['contato', 'endereco']
        fields = '__all__'
        # fields = ['nome']


class EquipamentosForm(forms.ModelForm):

    class Meta:
        model = Equipamento
        # exclude = ['status_chamado']
        fields = '__all__'  # ['status', 'tipo_chamado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].widget.attrs.update({'class': 'form-select'})
        self.fields['empresa'].empty_label = "Selecione uma Opção"


class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Endereco
        # exclude = ['status_chamado']
        fields = '__all__'  # ['status', 'tipo_chamado']



""" class CargaHorariaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaHorariaForm, self).__init__(*args, **kwargs)
        self.fields['data'].initial = datetime.now()

    class Meta:
        model = CargaHoraria
        # exclude = ['status_chamado']
        # '__all__'#['status', 'tipo_chamado']
        fields = ['data', 'hora_inicio', 'hora_termino', 'status']
        widgets = {
            'data': DatePicker(options={'useCurrent': True, 'collapse': True},
                               attrs={'append': 'fa fa-calendar', 'icon_toggle': True, }),

            'hora_inicio': TimePicker(options={"format": "HH:mm", 'defaultDate': '1970-01-01T08:00:00'
                                               }, attrs={'input_toggle': True, 'input_group': False, },),


            'hora_termino': TimePicker(options={"format": "HH:mm", 'defaultDate': '1970-01-01T18:00:00', "autoclose": True
                                                }, attrs={'input_toggle': True, 'input_group': False, },),



        } """
        
class CargaHorariaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CargaHorariaForm, self).__init__(*args, **kwargs)
        #self.fields['data'].initial = datetime.now()
        self.fields['data'].initial = datetime.now().strftime("%Y-%m-%d")
        self.fields['status'].widget.attrs['class'] = 'form-control form-select datetimefield'

    class Meta:
        model = CargaHoraria
        # exclude = ['status_chamado']
        # '__all__'#['status', 'tipo_chamado']
        fields = ['data', 'hora_inicio', 'hora_termino', 'status']
        
        widgets = {
            'data': forms.DateTimeInput(format='%Y-%m-%d', attrs={'type': 'date','class': 'form-control datetimefield' }),


            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '08:00', 'class': 'timefield form-control' }),


            'hora_termino': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '12:00', 'class': 'timefield form-control'}),           

            
        }

