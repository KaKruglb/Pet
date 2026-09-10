from django.contrib import admin
from .models import (
    Raca, Porte, Cor, Perfil, Tutor, Adotante, Admin as AdminModel, Pet, SolicitacaoAdocao,
)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("nome", "especie", "sexo", "status", "tutor", "ativo")
    list_filter = ("especie", "status", "ativo", "vacinado", "castrado")
    search_fields = ("nome", "descricao")


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ("user", "ativo")
    search_fields = ("user__username", "user__email")


@admin.register(Adotante)
class AdotanteAdmin(admin.ModelAdmin):
    list_display = ("user", "ativo")
    search_fields = ("user__username", "user__email")


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "telefone", "ativo")
    search_fields = ("user__username", "email", "cpf")


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ("pet", "adotante", "moradia", "tem_experiencia", "data_criacao")
    list_filter = ("moradia", "tem_experiencia", "outros_animais")
    search_fields = ("pet__nome", "adotante__user__username")


admin.site.register(Raca)
admin.site.register(Porte)
admin.site.register(Cor)
admin.site.register(AdminModel)
