from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('moviessapp:category_movies', args=[str(self.pk)])
    def __str__(self):
        return '{}'.format(self.name)
class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('moviessapp:deletemovie', args=[str(self.pk)])

    def __str__(self):
        return '{}'.format(self.title)