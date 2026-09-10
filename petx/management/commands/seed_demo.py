from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from petx.models import Raca, Porte, Cor, Perfil, Tutor, Adotante, Pet


class Command(BaseCommand):
    help = "Popula o banco com dados de exemplo para a demo da apresentação."

    def handle(self, *args, **options):
        # Lookups
        portes = {}
        for nome in ["Pequeno", "Médio", "Grande"]:
            portes[nome], _ = Porte.objects.get_or_create(porte=nome)

        cores = {}
        for nome in ["Caramelo", "Preto", "Branco", "Cinza", "Malhado"]:
            cores[nome], _ = Cor.objects.get_or_create(cor=nome)

        racas = {}
        for nome, especie in [("Sem raça definida", "C"), ("Sem raça definida (gato)", "G"), ("Labrador", "C")]:
            racas[nome], _ = Raca.objects.get_or_create(raca=nome, defaults={"especie": especie})

        # Tutor de demonstração
        user, created = User.objects.get_or_create(
            username="tutor_demo",
            defaults={"email": "tutor@devspets.com"},
        )
        if created:
            user.set_password("devspets123")
            user.save()

        perfil, _ = Perfil.objects.get_or_create(
            user=user,
            defaults={
                "email": "tutor@devspets.com",
                "telefone": "21999990000",
                "cpf": "11111111111",
                "data_nascimento": date(1995, 1, 1),
            },
        )
        tutor, _ = Tutor.objects.get_or_create(user=user, perfil=perfil)

        # Adotante de demonstração
        user2, created2 = User.objects.get_or_create(
            username="adotante_demo",
            defaults={"email": "adotante@devspets.com"},
        )
        if created2:
            user2.set_password("devspets123")
            user2.save()

        perfil2, _ = Perfil.objects.get_or_create(
            user=user2,
            defaults={
                "email": "adotante@devspets.com",
                "telefone": "21999990001",
                "cpf": "22222222222",
                "data_nascimento": date(1998, 5, 10),
            },
        )
        Adotante.objects.get_or_create(user=user2, perfil=perfil2)

        # Pets de exemplo
        pets_exemplo = [
            ("Mel", "C", "F", date(2023, 3, 1), "A Mel é uma cachorra muito carinhosa e tranquila."),
            ("Simba", "G", "M", date(2024, 6, 15), "Simba adora companhia e é bem brincalhão."),
            ("Amora", "C", "F", date(2022, 1, 10), "Amora é dócil e se dá bem com outros animais."),
            ("Thor", "C", "M", date(2021, 2, 20), "Thor é protetor e muito leal."),
            ("Luna", "G", "F", date(2023, 8, 5), "Luna é independente mas adora um colo."),
            ("Nina", "G", "F", date(2024, 1, 12), "Nina é curiosa e cheia de energia."),
        ]

        criados = 0
        for nome, especie, sexo, nascimento, descricao in pets_exemplo:
            pet, was_created = Pet.objects.get_or_create(
                nome=nome,
                tutor=tutor,
                defaults={
                    "especie": especie,
                    "sexo": sexo,
                    "nascimento": nascimento,
                    "descricao": descricao,
                    "vacinado": True,
                    "castrado": True,
                    "sociavel": True,
                    "status": "D",
                },
            )
            if was_created:
                criados += 1
                pet.porte.add(list(portes.values())[criados % 3])
                pet.cor.add(list(cores.values())[criados % len(cores)])

        self.stdout.write(self.style.SUCCESS(
            f"Seed concluído. {criados} pet(s) criado(s). "
            f"Login de teste -> tutor: tutor_demo / devspets123 | adotante: adotante_demo / devspets123"
        ))
