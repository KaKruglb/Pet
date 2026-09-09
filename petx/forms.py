import numbers

from django import forms
from .models import Pet, Raca, Cor, Porte, Especie, Status, Perfil, Instituicao, Anuncio, Tutor, Adotante, Endereco, Preferencia, Admin
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
            raise forms.ValidationError('CPF deve conter pelo menos 11 digitos')
        
        
        if len(cpf_digits) >= 11:
            raise forms.ValidationError('CPF deve conter apenas 11 digitos')
        
        
        if all(x == cpf_digits[0] for x in cpf_digits):
            raise forms.ValidationError('este CPF é inválido.')
        
        # fazendo checks para automaticamente verificar se um cpf escrito é real ou não, baseado no algoritmo de validação de CPF, ainda não está completo.
        
        if Perfil.objects.filter(cpf = cpf_digits).exists():
            raise forms.ValidationError('CPF registrado a outro usuario')
        
        
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
        
        
class InstituicaoForm(forms.ModelForm):
    # Manually declared fields, pulled in from Endereco
    cep = forms.CharField(max_length=9, label="CEP")
    logradouro = forms.CharField(max_length=200, label="Logradouro")
    numero = forms.CharField(max_length=10, label="Número")
    complemento = forms.CharField(max_length=100, required=False, label="Complemento")
    bairro = forms.CharField(max_length=100, label="Bairro")
    cidade = forms.CharField(max_length=100, label="Cidade")
    estado = forms.CharField(max_length=2, label="Estado")

    class Meta:
        model = Instituicao
        fields = ['nome', 'razao', 'tipo', 'cnpj', 'telefone', 'email']

    def save(self, commit=True):
        endereco = Endereco(
            cep=self.cleaned_data['cep'],
            logradouro=self.cleaned_data['logradouro'],
            numero=self.cleaned_data['numero'],
            complemento=self.cleaned_data['complemento'],
            bairro=self.cleaned_data['bairro'],
            cidade=self.cleaned_data['cidade'],
            estado=self.cleaned_data['estado'],
        )
        if commit:
            endereco.save()

        instituicao = super().save(commit=False)
        instituicao.endereco = endereco

        if commit:
            instituicao.save()

        return instituicao

class PreferenciaForm(forms.ModelForm):
    class Meta:
        model = Preferencia
        fields = ['especie', 'raca', 'porte', 'cor', 'sexo', 'castrado_sim', 'castrado_nao', 'vacinado', 'sociavel', 'idade']
        widgets = { 'sexo': forms.RadioSelect, 'castrado_sim': forms.RadioSelect, 'castrado_nao': forms.RadioSelect, 'vacinado': forms.RadioSelect, 'sociavel':forms.RadioSelect }