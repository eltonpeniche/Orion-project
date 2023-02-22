from django.urls import path

from . import views

urlpatterns = [
    path('tecnicos/', views.tecnicos, name='tecnicos'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('usuario_teste/', views.usuario_teste, name='usuario_teste'),
]
