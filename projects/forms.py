from django import forms
from .models import Project, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'external_link', 'image']
        labels = {
            'title': 'Название проекта',
            'description': 'Описание',
            'technologies': 'Технологии',
            'external_link': 'Внешняя ссылка',
            'image': 'Фотография проекта',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Введите название проекта'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Опишите ваш проект', 'rows': 5}),
            'technologies': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Например: Python, Django, React'}),
            'external_link': forms.URLInput(attrs={'class': 'input-field', 'placeholder': 'https://example.com'}),
            'image': forms.FileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'website', 'github']
        labels = {
            'avatar': 'Аватар',
            'bio': 'О себе',
            'location': 'Местоположение',
            'website': 'Веб-сайт',
            'github': 'GitHub username',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Расскажите о себе', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Город, страна'}),
            'website': forms.URLInput(attrs={'class': 'input-field', 'placeholder': 'https://example.com'}),
            'github': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'username'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'email@example.com'}))
    first_name = forms.CharField(required=False, label='Имя', widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ваше имя'}))
    last_name = forms.CharField(required=False, label='Фамилия', widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ваша фамилия'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Введите имя пользователя'}),
        }
