
from django import forms

from .models import TIPO_USUARIO, Usuario


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

    tipo_usuario = forms.ChoiceField(choices = TIPO_USUARIO.choices, label="Tipo de Usuário", initial='', widget=forms.Select(attrs={'class':'form-select'}), required=True)
                                    

   

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