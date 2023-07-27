import pytest

from movie_app.models import Genre, Person, Producer


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
