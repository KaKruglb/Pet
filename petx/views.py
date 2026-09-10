from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Perfil, Tutor, Adotante, Pet, Especie, Porte, SolicitacaoAdocao
from .forms import PetForm, SolicitacaoAdocaoForm


def home_view(request):
    disponiveis = Pet.objects.filter(ativo=True, status="D")
    pets_destaque = disponiveis.order_by("-id")[:6]
    return render(request, "home.html", {
        "pets_destaque": pets_destaque,
        "total_disponiveis": disponiveis.count(),
    })


def cadastro(request, tipo):
    """tipo = 'tutor' (quem doa) ou 'adotante' (quem adota)"""
    if tipo not in ("tutor", "adotante"):
        tipo = "adotante"

    erro = None

    if request.method == "POST":
        dados = request.POST
        cpf = dados.get("cpf", "")

        if Perfil.objects.filter(cpf=cpf).exists():
            erro = "Este CPF já está cadastrado."
        elif User.objects.filter(username=dados.get("username")).exists():
            erro = "Este nome de usuário já está em uso."
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
            messages.success(request, "Conta criada com sucesso! Bem-vindo(a) à DevsPets.")
            return redirect("meu_painel")

    return render(request, "cadastro/cadastro.html", {"erro": erro, "tipo": tipo})


def login_view(request):
    erro = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            messages.success(request, f"Bem-vindo(a) de volta, {user.username}!")
            return redirect("meu_painel")
        erro = "Usuário ou senha inválidos."
    return render(request, "conta/login.html", {"erro": erro})


def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect("login")


@login_required
def meu_painel(request):
    if hasattr(request.user, "tutor"):
        solicitacoes = SolicitacaoAdocao.objects.filter(pet__tutor=request.user.tutor).select_related("pet", "adotante__user").order_by("-data_criacao")
        return render(request, "conta/painel_tutor.html", {
            "pets": request.user.tutor.pets.filter(ativo=True),
            "solicitacoes": solicitacoes,
        })
    if hasattr(request.user, "adotante"):
        return render(request, "conta/painel_adotante.html")
    return redirect("home")

# --- Pet -----------------------------------------------------

def listar_pets(request):
    pets = Pet.objects.filter(ativo=True)

    q = request.GET.get("q")
    especie = request.GET.get("especie")
    porte = request.GET.get("porte")

    if q:
        pets = pets.filter(nome__icontains=q)
    if especie:
        pets = pets.filter(especie=especie)
    if porte:
        pets = pets.filter(porte__id=porte)

    return render(request, "pets/listar.html", {
        "pets": pets,
        "especies": Especie.choices,
        "portes": Porte.objects.all(),
        "q": q or "",
        "especie_sel": especie or "",
        "porte_sel": porte or "",
    })


def detalhe_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, ativo=True)
    pode_editar = request.user.is_authenticated and hasattr(request.user, "tutor") and pet.tutor.user == request.user
    precisa_adotante = request.GET.get("precisa_adotante") == "1"
    return render(request, "pets/detalhe.html", {"pet": pet, "pode_editar": pode_editar, "precisa_adotante": precisa_adotante})


@login_required
def criar_pet(request):
    if not hasattr(request.user, "tutor"):
        raise PermissionDenied

    form = PetForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        pet = form.save(commit=False)
        pet.tutor = request.user.tutor
        pet.save()
        form.save_m2m()  # necessário por causa dos campos ManyToMany (raca, cor, porte)
        messages.success(request, f"{pet.nome} foi cadastrado(a) com sucesso!")
        return redirect("detalhe_pet", pk=pet.pk)

    return render(request, "pets/form.html", {"form": form, "modo": "criar"})


@login_required
def editar_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if pet.tutor.user != request.user:
        raise PermissionDenied

    form = PetForm(request.POST or None, request.FILES or None, instance=pet)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Os dados de {pet.nome} foram atualizados.")
        return redirect("detalhe_pet", pk=pet.pk)

    return render(request, "pets/form.html", {"form": form, "modo": "editar", "pet": pet})


@login_required
def solicitar_adocao(request, pk):
    pet = get_object_or_404(Pet, pk=pk, ativo=True)

    if not hasattr(request.user, "adotante"):
        return redirect(f"{reverse('detalhe_pet', args=[pet.pk])}?precisa_adotante=1")

    if hasattr(request.user, "tutor") and pet.tutor.user == request.user:
        raise PermissionDenied

    adotante = request.user.adotante
    ja_enviou = SolicitacaoAdocao.objects.filter(pet=pet, adotante=adotante).exists()

    form = SolicitacaoAdocaoForm(request.POST or None)

    if not ja_enviou and request.method == "POST" and form.is_valid():
        solicitacao = form.save(commit=False)
        solicitacao.pet = pet
        solicitacao.adotante = adotante
        solicitacao.save()
        messages.success(request, f"Seu interesse em {pet.nome} foi enviado! O tutor vai poder ver suas respostas e entrar em contato.")
        return redirect("detalhe_pet", pk=pet.pk)

    return render(request, "pets/solicitar_adocao.html", {"pet": pet, "form": form, "ja_enviou": ja_enviou})


@login_required
def tornar_adotante(request, pk):
    """Cadastra o usuário logado como adotante na hora, sem formulário extra,
    para que ele possa enviar a solicitação de adoção imediatamente."""
    pet = get_object_or_404(Pet, pk=pk, ativo=True)

    if request.method == "POST" and not hasattr(request.user, "adotante"):
        if hasattr(request.user, "perfil"):
            Adotante.objects.get_or_create(user=request.user, perfil=request.user.perfil)
            messages.success(request, "Cadastro de adotante concluído! Agora você já pode enviar seu interesse.")
        else:
            messages.error(request, "Não foi possível concluir o cadastro automaticamente. Saia da conta e cadastre-se como adotante.")
            return redirect("detalhe_pet", pk=pet.pk)

    return redirect("solicitar_adocao", pk=pet.pk)


@login_required
def desativar_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if pet.tutor.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        pet.ativo = False
        pet.save()
        messages.success(request, f"{pet.nome} foi removido(a) da lista de adoção.")
        return redirect("meu_painel")

    return render(request, "pets/confirmar_desativacao.html", {"pet": pet})
