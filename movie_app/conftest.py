import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from movie_app.models import Genre, Person, Producer, Movie


@pytest.fixture
def genres():
    lst = []
    for x in range(5):
        lst.append(Genre.objects.create(name=x))
    return lst


@pytest.fixture
def persons():
    lst = []
    for x in range(5):
        lst.append(Person.objects.create(first_name=x, last_name=x, year=x))
    return lst


@pytest.fixture
def producers():
    lst = []
    for x in range(5):
        lst.append(Producer.objects.create(name=x, city=x, year=x))
    return lst


@pytest.fixture
def user():
    u = User.objects.create(username='testowy')
    return u
@pytest.fixture
def user_with_permission(user):
    content_type = ContentType.objects.get(app_label='movie_app',
                                           model='genre')
    permissions = Permission.objects.filter(content_type=content_type)
    user.user_permissions.set(permissions)
    return user

@pytest.fixture
def movies(producers, persons, genres):
    lst = []
    for x in range(5):
        m = Movie()
        m.title = x
        m.year = x
        m.director = persons[x]
        m.producer = producers[x]
        m.save()
        m.genre.set(genres)
        lst.append(m)
    return lst
