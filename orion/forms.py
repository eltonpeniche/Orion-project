from datetime import datetime

from django import forms
from tempus_dominus.widgets import DatePicker, DateTimePicker, TimePicker

from .models import (CargaHoraria, Contato, Empresa, Endereco, Equipamento,
                     Ordem_Servico, Usuario)


class OrdemServicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdemServicoForm, self).__init__(*args, **kwargs)
        self.fields['numero_chamado'].initial = datetime.now().strftime("%Y%m%d%H%M%S")
        self.fields['equipamento'].empty_label = "Selecione uma Opção"
        self.fields['empresa'].empty_label = "Selecione uma Opção"

    
    class Meta:
        model= Ordem_Servico
        exclude = ['status_chamado']
        #fields = '__all__'#['status', 'tipo_chamado']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model= Empresa
        exclude = ['contato', 'endereco']
        fields = '__all__'#
        #fields = ['nome']


class EquipamentosForm(forms.ModelForm):

    class Meta:
        model= Equipamento
        #exclude = ['status_chamado']
        fields = '__all__'#['status', 'tipo_chamado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].widget.attrs.update({'class': 'form-select'})
        self.fields['empresa'].empty_label = "Selecione uma Opção"

class EnderecoForm(forms.ModelForm):

    class Meta:
        model= Endereco
        #exclude = ['status_chamado']
        fields = '__all__'#['status', 'tipo_chamado']


class ContatoForm(forms.ModelForm):

    class Meta:
        model= Contato
        #exclude = ['status_chamado']
        fields = '__all__'#['status', 'tipo_chamado']


class CargaHorariaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaHorariaForm, self).__init__(*args, **kwargs)
        self.fields['data'].initial = datetime.now()
   
    class Meta:
        model= CargaHoraria
        #exclude = ['status_chamado']
        fields =  ['data', 'hora_inicio', 'hora_termino', 'status'] #'__all__'#['status', 'tipo_chamado']
        widgets = {
            'data' : DatePicker( options={ 'useCurrent': True, 'collapse': True },
                                 attrs={ 'append': 'fa fa-calendar', 'icon_toggle': True, }),
            
            'hora_inicio' : TimePicker(options={ "format": "HH:mm", 'defaultDate': '1970-01-01T08:00:00'
            },attrs={ 'input_toggle': True, 'input_group': False, },),

            
            'hora_termino' : TimePicker( options={"format": "HH:mm", 'defaultDate': '1970-01-01T18:00:00', "autoclose": True
            },attrs={ 'input_toggle': True, 'input_group': False, },),

        

        }

    
#Formulario de autenticação de usuários
class LoginForm(forms.Form):
    login = forms.CharField(
        label=False,
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Login', 'class':'form-control' }))
    
    senha = forms.CharField(
        label=False,
        max_length=100,
        required=True,
        widget = forms.PasswordInput(attrs={'placeholder':'Senha', 'class':'form-control'})
    )


class CadastroUsuarioForm(forms.Form):
    login = forms.CharField( label= "Usuário",
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Digite o nome de usuário', 'class':'form-control' })
        )
    email = forms.CharField( label= "Email",
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Digite o email', 'class':'form-control' })
        )

    senha = forms.CharField( label="Senha",
        max_length=100,
        required=True,
        widget = forms.PasswordInput(attrs={'placeholder':'Digite a senha', 'class':'form-control'}))

    
    confirmacao_senha = forms.CharField( label="Senha",
        max_length=100,
        required=True,
        widget = forms.PasswordInput(attrs={'placeholder':'Confirme a senha', 'class':'form-control'}))
        
    def clean_login(self):
        login = self.cleaned_data.get("login")
        if login:
            login = login.strip()
            if " " in login:
                raise forms.ValidationError("Login não pode conter espaços em branco")
            else:
                return login

    def clean_confirmacao_senha(self):
        senha = self.cleaned_data.get("senha")
        senha2 = self.cleaned_data.get("confirmacao_senha")
        if senha and senha2:
            if senha != senha2:
                raise forms.ValidationError("As senhas não podem ser diferentes")
            else:
                return senha2