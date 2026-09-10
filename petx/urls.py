from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    # Conta / autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/<str:tipo>/', views.cadastro, name='cadastro'),
    path('painel/', views.meu_painel, name='meu_painel'),

    # Pets (CRUD)
    path('pets/', views.listar_pets, name='listar_pets'),
    path('pets/novo/', views.criar_pet, name='criar_pet'),
    path('pets/<int:pk>/', views.detalhe_pet, name='detalhe_pet'),
    path('pets/<int:pk>/editar/', views.editar_pet, name='editar_pet'),
    path('pets/<int:pk>/excluir/', views.desativar_pet, name='desativar_pet'),
]
