from django.contrib import admin
from movie_app.models import Movie, Producer, Person, Comment, Genre
# Register your models here.

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Producer)
admin.site.register(Comment)
admin.site.register(Genre)