from django.contrib import admin

from moviessapp.models import Movie,Category

admin.site.register(Category)
admin.site.register(Movie)