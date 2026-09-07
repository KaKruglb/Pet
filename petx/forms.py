from django import forms
from .models import Pet, Raca, Cor, Porte, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PetForm(forms.ModelForm):
    
    class Meta:
        model = Pet
        fields =  ['descricao', 'nome', 'raca', 'cor', 'porte', 'sexo', 'vacinado', 'castrado' ]
        widgets = { 'sexo': forms.RadioSelect, 'vacinado': forms.RadioSelect, 'castrado': forms.RadioSelect }
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].label = "Usuário"
        
        self.fields['password1'].help_text = None
        self.fields['password1'].label = "Senha"
        
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirmar Senha"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [ 'email', 'telefone', 'cpf', 'data_nascimento' ]
        widgets = { 'data_nascimento': forms.DateInput(attrs={'type': 'date'}), }
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Perfil.objects.filter(cpf = cpf).exists():
            raise forms.ValidationError('CPF registrado a outro usuario')
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(emial = email).exists():
            raise forms.ValidationError('Email registrado a outro usuario')
        return email

        