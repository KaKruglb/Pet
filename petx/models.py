from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Especie(models.Model):
    especie = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.especie

class Raca(models.Model): 
    raca = models.CharField(max_length = 100, unique = True)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="racas")
    
    def __str__(self):
        return self.raca
    
class Porte(models.Model): 
    porte = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.porte
    
    
class Status(models.Model):
    status = models.CharField(max_length = 200, unique = True)
    
    def __str__(self):
        return self.status
    
    
    
class Cor(models.Model): 
    cor = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.cor
    
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    email = models.EmailField(unique=True, blank = False)
    telefone = models.CharField(max_length=20, blank = False, unique = True)
    cpf = models.CharField(max_length=14, unique=True, blank = False)
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
    
    

class Pet(models.Model): 
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="pets")
    nome = models.CharField(max_length=15)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="pets", null=True, blank=True)
    raca = models.ManyToManyField(Raca, related_name="pets", blank=True)
    castrado = models.BooleanField(default=False)
    vacinado = models.BooleanField(default=False)
    sociavel = models.BooleanField(default=False)
    nascimento = models.DateField(default=date.today)
    descricao = models.CharField(max_length=1500)
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        FEMEA = "F", "Femea"
    sexo = models.CharField(max_length = 1, choices = Sexo.choices)
    porte = models.ManyToManyField(Porte, related_name="pets", blank=True)
    cor = models.ManyToManyField(Cor, related_name="pets", blank=True)
    status = models.CharField(max_length=200, choices=Status.choices)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    


class Instituicao(models.Model):
    razao = models.CharField(max_length=500)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=200)
    email = models.EmailField(unique=True, blank = False)
    telefone = models.CharField(max_length=20, blank = False, unique = True)
    cnpj = models.CharField(max_length=18, unique=True, blank = False)
    endereco = models.OneToOneField('Endereco', on_delete=models.CASCADE, related_name="instituicao", null=True, blank=True)
    status = models.BooleanField(default=True)    
    
    
    
class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

 
 
   
class Anuncio(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name="anuncios")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="anuncios")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="anuncios")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    
class Preferencias(models.Model):
    adotante = models.OneToOneField(Adotante, on_delete=models.CASCADE, related_name="preferencias")
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    porte = models.ForeignKey(Porte, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE, related_name="preferencias", blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=Pet.Sexo.choices, blank=True)
    castrado = models.BooleanField(default=False)
    vacinado = models.BooleanField(default=False)
    sociavel = models.BooleanField(default=False)
    idade = models.IntegerField(blank=True, null=True)