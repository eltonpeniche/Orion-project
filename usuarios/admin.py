from django.contrib import admin
from django.contrib.auth.models import User

from .models import Usuario

# Register your models here.


# Register your models here.


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','user','tipo' )
    ordering = ('id',)

    
