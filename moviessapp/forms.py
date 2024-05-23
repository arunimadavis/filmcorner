from django import forms
from django.contrib.auth.models import User
from .models import Movie
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']