import pytest
from django.test import Client
from django.urls import reverse

from movie_app.forms import SearchPersonForm, AddPersonForm, AddMovieModelForm
from movie_app.models import Person, Producer, Movie, Comment


@pytest.mark.django_db
def test_index():
    przegladarka = Client()
    url = reverse('index')
    response = przegladarka.get(url)
    content = str(response.content)
    assert '<a href="/listMovie/">filmy</a>' in content
    assert response.status_code == 200


@pytest.mark.django_db
def test_genre_list(genres):
    browser = Client()
    url = reverse('list_genre')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['genres'].count() == len(genres)


@pytest.mark.django_db
def test_person_list(persons):
    browser = Client()
    url = reverse('list_person')
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['persons'].count() == len(persons)
    assert isinstance(response.context['form'], SearchPersonForm)
    for person in persons:
        assert person in response.context['persons']


@pytest.mark.django_db
def test_person_search(persons):
    browser = Client()
    url = reverse('list_person')
    data = {'first_name': '1',
            'last_name': '1',
            'year': 1}
    response = browser.get(url, data)
    assert response.status_code == 200
    assert response.context['persons'].get(**data)


@pytest.mark.django_db
def test_producer_list_view(producers):
    browser = Client()
    url = reverse('list_producer')
    response = browser.get(url)
    assert response.status_code == 200
    assert list(response.context['producers']) == producers


@pytest.mark.django_db
def test_producer_detail_view(producers):
    browser = Client()
    p = producers[0]
    url = reverse('detail_producer', kwargs={'id': p.id})
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['producer'] == p


@pytest.mark.django_db
def test_detail_genre_view_not_login(genres):
    browser = Client()
    g = genres[0]
    url = reverse('detail_genre', args=(g.id,))
    # browser.force_login(user)
    response = browser.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_detail_genre_view_login_without_permission(genres, user):
    browser = Client()
    g = genres[0]
    url = reverse('detail_genre', args=(g.id,))
    browser.force_login(user)
    response = browser.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_detail_genre_view_login_with_permission(genres, user_with_permission):
    browser = Client()
    g = genres[0]
    url = reverse('detail_genre', args=(g.id,))
    browser.force_login(user_with_permission)
    response = browser.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_movie_list_view(movies):
    browser = Client()
    url = reverse('list_movie')
    response = browser.get(url)
    assert response.status_code == 200
    assert list(response.context['movies']) == movies


@pytest.mark.djnago_db
def test_add_person_get():
    browser = Client()
    url = reverse('add_person')
    response = browser.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPersonForm)


@pytest.mark.django_db
def test_add_person_post():
    browser = Client()
    url = reverse('add_person')
    data = {
        'first_name': 'sla',
        'last_name': 'bo',
        'year': 1293
    }
    response = browser.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('add_person'))
    assert Person.objects.get(**data)


@pytest.mark.django_db
def test_add_producer_get():
    browser = Client()
    url = reverse('add_producer')
    response = browser.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_producer_post():
    browser = Client()
    url = reverse('add_producer')
    data = {
        'name': 'Py',
        'city': 'Ton',
        'year': 1921
    }
    response = browser.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('add_producer'))
    assert Producer.objects.get(**data)


@pytest.mark.django_db
def test_get_add_movie():
    browser = Client()
    url = reverse('add_movie')
    response = browser.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddMovieModelForm)

@pytest.mark.django_db
def test_post_add_movie(persons, producers, genres):
    browser = Client()
    url = reverse('add_movie')
    data = {
        'title':'ptysi mysie',
        'year': 1999,
        'director':persons[0].id,
        'producer':producers[0].id,
        'genre':[x.id for x in genres]
    }
    response = browser.post(url, data)
    assert response.status_code == 302
    del data['genre']
    obj = Movie.objects.get(**data)
    assert list(obj.genre.all()) == genres


@pytest.mark.django_db
def test_add_comment_to_movie(movies, user):
    movie = movies[0]
    browser = Client()
    url = reverse('add_comment', args=(movie.id, ))
    browser.force_login(user)
    data = {
        'text':'ala ma kota'
    }
    response = browser.post(url, data)
    assert response.status_code == 302
    assert Comment.objects.get(**data)
