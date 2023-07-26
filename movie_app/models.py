from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=123)
    last_name = models.CharField(max_length=123)
    year = models.IntegerField()

    def get_detail_url(self):
        return reverse('detail_person', kwargs={'id':self.id})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=123)


    def get_detail_url(self):
        return reverse('detail_genre', kwargs={'id':self.id})

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=123)
    city = models.CharField(max_length=123)
    year = models.IntegerField()

    def get_detail_url(self):
        return reverse('detail_producer', kwargs={'id':self.id})

    def __str__(self):
        return f"{self.name} {self.city}"


class Movie(models.Model):
    title = models.CharField(max_length=123)
    year = models.IntegerField()
    director = models.ForeignKey(Person, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    def get_detail_url(self):
        return reverse('detail_movie', kwargs={'id':self.id})

    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie} {self.text[:10]}"

