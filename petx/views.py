import re
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Perfil, Tutor, Adotante
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, Anuncio, Instituicao, Preferencia
from .forms import PetForm, AnuncioForm, InstituicaoForm, PreferenciaForm



def cadastro(request, tipo):
    """tipo = 'tutor' ou 'adotante'"""
    erro = None

    if request.method == "POST":
        dados = request.POST
        cpf = dados.get("cpf")

        if Perfil.objects.filter(cpf=cpf).exists():
            erro = "Este CPF já está cadastrado."
        else:
            user = User.objects.create_user(
                username=dados["username"], email=dados["email"], password=dados["password"]
            )
            perfil = Perfil.objects.create(
                user=user, email=dados["email"], telefone=dados["telefone"],
                cpf=cpf, data_nascimento=dados["data_nascimento"],
            )
            (Tutor if tipo == "tutor" else Adotante).objects.create(user=user, perfil=perfil)
            login(request, user)
            return redirect("meu_painel")

    return render(request, f"cadastro/cadastro_{tipo}.html", {"erro": erro})


def login_view(request):
    erro = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("meu_painel")
        erro = "Usuário ou senha inválidos."
    return render(request, "conta/login.html", {"erro": erro})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def meu_painel(request):
    if hasattr(request.user, "tutor"):
        return render(request, "conta/painel_tutor.html", {"pets": request.user.tutor.pets.filter(ativo=True)})
    if hasattr(request.user, "adotante"):
        return render(request, "conta/painel_adotante.html")
    return redirect("home")


@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    erro = None

    if request.method == "POST":
        cpf = request.POST.get("cpf", perfil.cpf)

        if cpf != perfil.cpf and Perfil.objects.filter(cpf=cpf).exists():
            erro = "Este CPF já está cadastrado."
        else:
            perfil.email = request.POST.get("email", perfil.email)
            perfil.telefone = request.POST.get("telefone", perfil.telefone)
            perfil.cpf = cpf
            perfil.save()
            return redirect("meu_painel")

    return render(request, "conta/editar_perfil.html", {"perfil": perfil, "erro": erro})

# --- Pet -----------------------------------------------------

def listar_pets(request):
    pets = Pet.objects.filter(ativo=True)

    especie = request.GET.get("especie")
    porte = request.GET.get("porte")

    if especie:
        pets = pets.filter(especie__id=especie)
    if porte:
        pets = pets.filter(porte__id=porte)

    return render(request, "pets/listar.html", {"pets": pets})


def detalhe_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, ativo=True)
    return render(request, "pets/detalhe.html", {"pet": pet})


@login_required
def criar_pet(request):
    if not hasattr(request.user, "tutor"):
        raise PermissionDenied

    form = PetForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        pet = form.save(commit=False)
        pet.tutor = request.user.tutor
        pet.save()
        form.save_m2m()  # necessário por causa dos campos ManyToMany (raca, cor, porte)
        return redirect("detalhe_pet", pk=pet.pk)

    return render(request, "pets/form.html", {"form": form})


@login_required
def editar_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if pet.tutor.user != request.user:
        raise PermissionDenied

    form = PetForm(request.POST or None, instance=pet)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("detalhe_pet", pk=pet.pk)

    return render(request, "pets/form.html", {"form": form})


@login_required
def desativar_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if pet.tutor.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        pet.ativo = False
        pet.save()
        return redirect("meu_painel")

    return render(request, "pets/confirmar_desativacao.html", {"pet": pet})


# --- Anúncio ----------------------------------------------------

def listar_anuncios(request):
    anuncios = Anuncio.objects.filter(ativo=True)
    return render(request, "anuncios/listar.html", {"anuncios": anuncios})


def detalhe_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, ativo=True)
    return render(request, "anuncios/detalhe.html", {"anuncio": anuncio})


@login_required
def criar_anuncio(request):
    if not hasattr(request.user, "tutor"):
        raise PermissionDenied

    form = AnuncioForm(request.POST or None)
    # o tutor só pode anunciar os próprios pets
    form.fields["pet"].queryset = request.user.tutor.pets.filter(ativo=True)

    if request.method == "POST" and form.is_valid():
        anuncio = form.save(commit=False)
        anuncio.tutor = request.user.tutor
        anuncio.save()
        return redirect("detalhe_anuncio", pk=anuncio.pk)

    return render(request, "anuncios/form.html", {"form": form})


@login_required
def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)

    if anuncio.tutor.user != request.user:
        raise PermissionDenied

    form = AnuncioForm(request.POST or None, instance=anuncio)
    form.fields["pet"].queryset = request.user.tutor.pets.filter(ativo=True)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("detalhe_anuncio", pk=anuncio.pk)

    return render(request, "anuncios/form.html", {"form": form})


@login_required
def encerrar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)

    if anuncio.tutor.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        anuncio.ativo = False
        anuncio.save()
        return redirect("meu_painel")

    return render(request, "anuncios/confirmar_encerramento.html", {"anuncio": anuncio})


# --- Preferência (do Adotante) -----------------------------------

@login_required
def definir_preferencias(request):
    if not hasattr(request.user, "adotante"):
        raise PermissionDenied

    preferencia, _ = Preferencia.objects.get_or_create(adotante=request.user.adotante)
    form = PreferenciaForm(request.POST or None, instance=preferencia)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("meu_painel")

    return render(request, "conta/preferencias.html", {"form": form})
