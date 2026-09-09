from django import forms
from .models import Pet, Raca, Cor, Porte, Especie, Perfil, Anuncio, Preferencia, Mensagem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PetForm(forms.ModelForm):
    
    class Meta:
        model = Pet
        fields =  ['descricao', 'nome', 'raca', 'cor', 'porte', 'sexo', 'vacinado', 'castrado', 'sociavel', 'especie', 'nascimento', 'status']
        widgets = { 'sexo': forms.RadioSelect, 'vacinado': forms.RadioSelect, 'castrado': forms.RadioSelect, 'sociavel':forms.RadioSelect, 'nascimento': forms.DateInput(attrs={'type': 'date'}) }
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ("username", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].label = "Usuário"
        
        self.fields['password1'].help_text = None
        self.fields['password1'].label = "Senha"
        
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirmar Senha"

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [ 'email', 'telefone', 'cpf', 'data_nascimento' ]
        widgets = { 'data_nascimento': forms.DateInput(attrs={'type': 'date'}), }
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf_digits = ''.join(char for char in cpf if char.isdigit())
        
        if len(cpf_digits) != 11:
            raise forms.ValidationError('CPF deve conter exatamente 11 digitos')
        
        if all(x == cpf_digits[0] for x in cpf_digits):
            raise forms.ValidationError('este CPF é inválido.')
        
        if Perfil.objects.filter(cpf = cpf_digits).exists():
            raise forms.ValidationError('CPF já registrado a outro usuario')
        
        return cpf_digits
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Perfil.objects.filter(email = email).exists():
            raise forms.ValidationError('Email registrado a outro usuario')
        return email


class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'pet', 'status']
        

class PreferenciaForm(forms.ModelForm):
    class Meta:
        model = Preferencia
        fields = ['especie', 'raca', 'porte', 'cor', 'sexo', 'castrado_sim', 'castrado_nao', 'vacinado', 'sociavel', 'idade']
        widgets = { 'sexo': forms.RadioSelect, 'castrado_sim': forms.RadioSelect, 'castrado_nao': forms.RadioSelect, 'vacinado': forms.RadioSelect, 'sociavel':forms.RadioSelect }


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['conteudo']
        widgets = { 'conteudo': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Digite sua mensagem...'}) }