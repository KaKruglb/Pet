from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Especie(models.TextChoices):
    CACHORRO = "C", "Cachorro"
    GATO = "G", "Gato"

class Raca(models.Model): 
    raca = models.CharField(max_length=100, unique=True)
    especie = models.CharField(max_length=1, choices=Especie.choices)
    
    def __str__(self):
        return self.raca
    
class Porte(models.Model): 
    porte = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.porte
     
    
class Cor(models.Model): 
    cor = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.cor
    
    
class Status(models.TextChoices):
    DISPONIVEL = "D", "Disponível"
    EM_ANDAMENTO = "A", "Em andamento"
    INDISPONIVEL = "I", "Indisponível"
    
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    imagem = models.CharField(max_length=500, blank=True)
    email = models.EmailField(unique=True, blank = False)
    telefone = models.CharField(max_length=20, blank = False, unique = True)
    cpf = models.CharField(max_length=11, unique=True, blank = False)
    data_nascimento = models.DateField(blank = False)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tutor")
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="tutor")
    ativo = models.BooleanField(default=True)


class Adotante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="adotante")
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="adotante")
    ativo = models.BooleanField(default=True)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name="admin")
    ativo = models.BooleanField(default=True)
    

class Pet(models.Model): 
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="pets")
    imagem = models.CharField(max_length=500, blank=True)
    nome = models.CharField(max_length=15)
    especie = models.CharField(max_length=1, choices=Especie.choices, default=Especie.CACHORRO)
    raca = models.ManyToManyField(Raca, related_name="pets", blank=True)
    castrado = models.BooleanField(default=False)
    vacinado = models.BooleanField(default=False)
    sociavel = models.BooleanField(default=False)
    nascimento = models.DateField(blank = False)
    descricao = models.CharField(max_length=1500)
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        FEMEA = "F", "Femea"
    sexo = models.CharField(max_length = 1, choices = Sexo.choices)
    porte = models.ManyToManyField(Porte, related_name="pets", blank=True)
    cor = models.ManyToManyField(Cor, related_name="pets", blank=True)
    status = models.CharField(max_length=1, choices=Status.choices, default="D")
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
   
class Anuncio(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="anuncios", null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="anuncios")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=Status.choices, default="D")
    ativo = models.BooleanField(default=True)
    
    
class Preferencia(models.Model):
    adotante = models.OneToOneField(Adotante, on_delete=models.CASCADE, related_name="preferencias")
    especie = models.CharField(max_length=1, choices=Especie.choices, blank=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    porte = models.ForeignKey(Porte, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=Pet.Sexo.choices, blank=True)
    castrado_sim = models.BooleanField(default=True)
    castrado_nao = models.BooleanField(default=True)
    vacinado = models.BooleanField(default=False)
    sociavel = models.BooleanField(default=False)
    idade = models.IntegerField(blank=True, null=True)


class Conversa(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name="conversas")
    adotante = models.ForeignKey(Adotante, on_delete=models.CASCADE, related_name="conversas")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)



class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name="mensagens")
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    