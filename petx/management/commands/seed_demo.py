from datetime import date

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from petx.models import Raca, Porte, Cor, Perfil, Tutor, Adotante, Pet

try:
    import requests
except ImportError:
    requests = None


DOG_URL = "https://placedog.net/640/480?id={n}"
CAT_URL = "https://cataas.com/cat?width=640&height=480&t={n}"


def baixar_foto(especie, n):
    """Tenta baixar uma foto real de cachorro/gato. Se não houver internet
    disponível (ex: ambiente sem acesso externo), retorna None e o site usa
    o ícone ilustrativo no lugar — não quebra o seed."""
    if requests is None:
        return None
    url = DOG_URL.format(n=n) if especie == "C" else CAT_URL.format(n=n)
    try:
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200 and resp.content:
            return ContentFile(resp.content, name=f"{especie}_{n}.jpg")
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = "Popula o banco com dados de exemplo (pets, raças, tutor/adotante de teste) para a demo."

    def handle(self, *args, **options):
        # Lookups de porte e cor
        portes = {}
        for nome in ["Pequeno", "Médio", "Grande"]:
            portes[nome], _ = Porte.objects.get_or_create(porte=nome)

        cores = {}
        for nome in ["Caramelo", "Preto", "Branco", "Cinza", "Malhado", "Tricolor"]:
            cores[nome], _ = Cor.objects.get_or_create(cor=nome)

        # Raças (dão a variedade de "espécies" pedida na demo)
        racas_info = [
            ("Labrador", "C"), ("Poodle", "C"), ("Bulldog Francês", "C"),
            ("Golden Retriever", "C"), ("Vira-lata Caramelo", "C"),
            ("Pastor Alemão", "C"), ("Beagle", "C"), ("Shih Tzu", "C"),
            ("Siamês", "G"), ("Persa", "G"), ("Maine Coon", "G"),
            ("Vira-lata (SRD)", "G"), ("Angorá", "G"), ("Sphynx", "G"),
            ("Ragdoll", "G"),
        ]
        racas = {}
        for nome, especie in racas_info:
            racas[nome], _ = Raca.objects.get_or_create(raca=nome, defaults={"especie": especie})

        # Tutor de demonstração
        user, created = User.objects.get_or_create(
            username="tutor_demo", defaults={"email": "tutor@devspets.com"}
        )
        if created:
            user.set_password("devspets123")
            user.save()

        perfil, _ = Perfil.objects.get_or_create(
            user=user,
            defaults={
                "email": "tutor@devspets.com", "telefone": "21999990000",
                "cpf": "11111111111", "data_nascimento": date(1995, 1, 1),
            },
        )
        tutor, _ = Tutor.objects.get_or_create(user=user, perfil=perfil)

        # Adotante de demonstração
        user2, created2 = User.objects.get_or_create(
            username="adotante_demo", defaults={"email": "adotante@devspets.com"}
        )
        if created2:
            user2.set_password("devspets123")
            user2.save()

        perfil2, _ = Perfil.objects.get_or_create(
            user=user2,
            defaults={
                "email": "adotante@devspets.com", "telefone": "21999990001",
                "cpf": "22222222222", "data_nascimento": date(1998, 5, 10),
            },
        )
        Adotante.objects.get_or_create(user=user2, perfil=perfil2)

        # 15 pets de exemplo, um pra cada raça acima
        pets_exemplo = [
            ("Mel", "Labrador", "F", date(2023, 3, 1), "A Mel é uma cachorra muito carinhosa e tranquila."),
            ("Duke", "Poodle", "M", date(2022, 7, 12), "Duke adora um carinho atrás da orelha."),
            ("Bento", "Bulldog Francês", "M", date(2021, 11, 3), "Bento é tranquilo e ótimo companheiro de sofá."),
            ("Thor", "Golden Retriever", "M", date(2021, 2, 20), "Thor é protetor e muito leal."),
            ("Amora", "Vira-lata Caramelo", "F", date(2022, 1, 10), "Amora é dócil e se dá bem com outros animais."),
            ("Fred", "Pastor Alemão", "M", date(2020, 6, 5), "Fred é esperto e cheio de energia."),
            ("Nala", "Beagle", "F", date(2023, 9, 18), "Nala é curiosa e adora explorar."),
            ("Zeus", "Shih Tzu", "M", date(2022, 4, 22), "Zeus é pequeno mas cheio de personalidade."),
            ("Simba", "Siamês", "M", date(2024, 6, 15), "Simba adora companhia e é bem brincalhão."),
            ("Luna", "Persa", "F", date(2023, 8, 5), "Luna é independente mas adora um colo."),
            ("Nina", "Maine Coon", "F", date(2024, 1, 12), "Nina é curiosa e cheia de energia."),
            ("Mia", "Vira-lata (SRD)", "F", date(2022, 10, 30), "Mia é carinhosa e se adapta fácil a qualquer casa."),
            ("Bela", "Angorá", "F", date(2021, 12, 8), "Bela é elegante e gosta de observar tudo de longe."),
            ("Max", "Sphynx", "M", date(2023, 2, 14), "Max é super sociável e adora atenção."),
            ("Lola", "Ragdoll", "F", date(2022, 5, 27), "Lola é dócil e ama dormir no colo."),
        ]

        criados = 0
        sem_foto = 0
        for i, (nome, raca_nome, sexo, nascimento, descricao) in enumerate(pets_exemplo, start=1):
            raca = racas[raca_nome]
            pet, was_created = Pet.objects.get_or_create(
                nome=nome,
                tutor=tutor,
                defaults={
                    "especie": raca.especie,
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
                pet.raca.add(raca)
                pet.porte.add(list(portes.values())[i % 3])
                pet.cor.add(list(cores.values())[i % len(cores)])

                foto = baixar_foto(raca.especie, i)
                if foto:
                    pet.imagem.save(foto.name, foto, save=True)
                else:
                    sem_foto += 1

        msg = f"Seed concluído. {criados} pet(s) criado(s)."
        if criados and sem_foto:
            msg += f" {sem_foto} sem foto (sem internet disponível agora) — o site usa um ícone no lugar."
        msg += " Login de teste -> tutor: tutor_demo / devspets123 | adotante: adotante_demo / devspets123"
        self.stdout.write(self.style.SUCCESS(msg))
