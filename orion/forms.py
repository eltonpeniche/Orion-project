import re
from datetime import datetime

from django import forms
from validate_docbr import CNPJ

from .models import CargaHoraria, Empresa, Endereco, Equipamento, Ordem_Servico


class OrdemServicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['numero_chamado'].initial = datetime.now().strftime(
            "%Y%m%d%H%M%S")
        #self.fields['equipamento'].empty_label = "Selecione uma Opção"
        #self.fields['empresa'].empty_label = "Selecione uma Opção"
        self.fields['empresa'].widget.attrs.update({'class':'select2' })
        self.fields['equipamento'].widget.attrs.update({'class':'select2' })
    class Meta:
        model = Ordem_Servico
        exclude = ['status_chamado', 'aberto_por']
        # fields = '__all__'#['status', 'tipo_chamado']


class EmpresaForm(forms.ModelForm):
    
    cnpj  = forms.CharField(max_length=18)
    telefone  = forms.CharField(max_length=15)
    
    class Meta:
        model = Empresa
        exclude = ['contato', 'endereco']
        fields = '__all__'
     
    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.fields['cnpj'].widget.attrs.update({'class':'cnpj' })
        self.fields['telefone'].widget.attrs.update({'class':'telefone' })
    
    def clean_cnpj(self):
        valida_cnpj = CNPJ()
        cnpj = self.cleaned_data.get('cnpj')
        cnpj = re.sub(r"\D", "", cnpj)
        print(cnpj, len(cnpj))
        if valida_cnpj.validate(cnpj):
            return cnpj
        raise forms.ValidationError("CNPJ informado não é válido")
    
        
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        telefone = re.sub(r"\D", "", telefone)
        if len(telefone) == 10 or len(telefone) == 11:
            return telefone

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

    cep  = forms.CharField(max_length=9)
    
    class Meta:
        model = Endereco
        # exclude = ['status_chamado']
        fields = ['cep','rua','bairro','uf','cidade', 'numero'] 
    
    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs.update({'class':'cep'})
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        cep = re.sub(r"\D", "", cep)
        print(cep, len(cep))
        if len(cep) == 8:
            return cep


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
        #self.fields['status'].widget.attrs.update({'class':''})

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
    
    def clean(self):
        cleaned_data = super().clean()
        
        data = cleaned_data.get('data')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_termino = cleaned_data.get('hora_termino')

        if self.instance.ordem_servico:
            #carregando todos os horarios relacionados com a instancia de ordem_servico
            lista_carga_horaria = CargaHoraria.objects.select_related('ordem_servico').filter(ordem_servico=self.instance.ordem_servico.pk).filter(data=data)

            for ch in lista_carga_horaria:
                if ch.data == data:
                    if horarios_se_sobrepoe(hora_inicio, hora_termino, ch.hora_inicio, ch.hora_termino):
                        if self.instance.pk:    
                            if ch.id != self.instance.pk:
                                raise forms.ValidationError({'hora_inicio':"As datas não podem ser iguais"})
                        else:
                            raise forms.ValidationError({'hora_inicio':"As datas não podem ser iguais"})
                    

 


def horarios_se_sobrepoe(h1_inicio, h1_fim, h2_inicio, h2_fim):
    if h1_inicio <= h2_inicio < h1_fim or h2_inicio <= h1_inicio < h2_fim:
        return True
    return False