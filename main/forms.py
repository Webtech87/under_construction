from django import forms
from django.db import models

class ContactRequestForm(forms.Form):
    
    class Subjects(models.TextChoices):
        SELECT = 'Assunto', 'Assunto'
        BOOKS  = 'Livros', 'Livros'
        COURSES = 'Cursos', 'Cursos'
        MENTORSHIP = 'Mentorias', 'Mentorias'
        IMMERSIONS = 'Imerções', 'Imerções'

    full_name = forms.CharField(
        label='Nome:',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control white-border', 'placeholder': 'Insira o seu nome', 'style': 'border-radius: 8px;'})        
        )
    email = forms.EmailField(
        label='Email:',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control white-border', 'placeholder': 'Insira o seu email', 'style': 'border-radius: 8px;'})        
    )
    subject = forms.ChoiceField(
        label='Assunto:',
        choices = Subjects.choices,
        initial= Subjects.SELECT,
        widget=forms.Select(attrs={'class': 'form-control white-border', 'style': 'border-radius: 8px;'})        
    )
    message = forms.CharField(
        label='Mensagem:',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control white-border', 'rows': 5, 'cols': 40, 'placeholder': 'Escreva aqui a sua mensagem', 'style': 'border-radius: 8px;'})        
    )
    accept_terms = forms.BooleanField(
        label='',        
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'exampleCheck'})        
    )