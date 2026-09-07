from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Raca(models.Model): 
    raca = models.CharField(max_length = 100, unique = True)
    
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

class Pet(models.Model): 
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    nome = models.CharField(max_length=15)
    raca = models.ManyToManyField(Raca, related_name="pets", blank=True)
    castrado = models.BooleanField(default=False)
    vacinado = models.BooleanField(default=False)
    nascimento = models.DateField(default=date.today)
    descricao = models.CharField(max_length=1500)
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        FEMEA = "F", "Femea"
    sexo = models.CharField(max_length = 1, choices = Sexo.choices)
    porte = models.ManyToManyField(Porte, related_name="pets", blank=True)
    cor = models.ManyToManyField(Cor, related_name="pets", blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    email = models.EmailField(unique=True, blank = False)
    telefone = models.CharField(max_length=20, blank = False)
    cpf = models.CharField(max_length=14, unique=True, blank = False)
    data_nascimento = models.DateField(blank = False)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username