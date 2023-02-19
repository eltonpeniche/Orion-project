from django.contrib import admin

from .models import Usuario

# Register your models here.


# Register your models here.


class UsuarioAdmin(admin.ModelAdmin):
    ...


admin.site.register(Usuario, UsuarioAdmin)
