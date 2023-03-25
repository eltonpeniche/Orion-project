from usuarios.models import User, Usuario


class OrionMixin:
    def make_usuario(self, login='elton', 
                     nome='Elton', 
                     sobrenome = 'Peniche', 
                     email = 'elton@email.com', 
                     senha = '@Bc123456', 
                     tipo='A'                   ):
        
        user = User.objects.create_user(
            first_name=nome,
            last_name=sobrenome,
            username=login,
            password=senha,
            email=email,
        )
        usuario = Usuario.objects.create(
            user = user,
            tipo = tipo
        )
        return user, usuario
    
    #def make_chamado(self):
