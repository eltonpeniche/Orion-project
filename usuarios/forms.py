
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

class UserUpdateForm(UserChangeForm):
    password = forms.CharField( label='Senha', help_text= '* Ao deixar este campo vazio, a senha atual será mantida', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
    password2 = forms.CharField( label='Confirmar Senha', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        readonly_fields = ('first_name', )
        labels = {
            'username': 'Login',  # Alterar o label do campo 
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
    
    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        print("password2 = ",password2)
        print("cleaned_data = ",self.cleaned_data)
        
        if not password and not password2:
            # Mantém a senha atual se o campo de senha estiver vazio
            #print(self.instance.password)
            return None
        
        if password != password2:
            raise forms.ValidationError("As senhas não podem ser diferentes")

        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
        return user


class UsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['tipo'].widget.attrs['readonly'] = True
        #self.fields['tipo'].widget.attrs['disabled'] = True
        self.fields['tipo'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Usuario
        fields = ['tipo']



class CadastroUsuarioForm(forms.Form):
    nome = forms.CharField( label= "Nome",
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Digite o nome', 'class':'form-control' })
    )

    sobrenome = forms.CharField( label= "Sobrenome",
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Digite o sobrenome', 'class':'form-control' })
    )
    
    login = forms.CharField( label= "Login",
        max_length=100,
        required=True,
        widget= forms.TextInput(attrs={'placeholder':'Digite o login', 'class':'form-control' })
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

    tipo_usuario = forms.ChoiceField(choices = TIPO_USUARIO.choices, label="Tipo de Usuário", initial='T', widget=forms.Select(attrs={'class':'form-select'}), required=True)
                                    

   

    def clean_login(self):
        login = self.cleaned_data.get("login")
        if login:
            login = login.strip()
            if " " in login:
                raise forms.ValidationError("Login não pode conter espaços em branco")
            else:
                return login

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha2 = cleaned_data.get('confirmacao_senha')
        if senha != senha2:
            raise forms.ValidationError({'confirmacao_senha':"As senhas não podem ser diferentes"})
        else:
            return senha2
        
            

