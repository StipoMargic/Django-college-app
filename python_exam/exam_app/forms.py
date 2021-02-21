from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Korisnik, Predmet, Upisi


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')
    class Meta:
        model = Korisnik
        fields = ("email", "username", 'status', "password1", "password2")


class PredmetForm(ModelForm):
    class Meta:
        model = Predmet
        fields = ('ime', 'kod', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni')


class UpisiForm(ModelForm):
    class Meta:
        model = Upisi
        fields = ('student', 'predmet', 'status')
