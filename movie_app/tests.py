import pytest
from django.test import Client
from django.urls import reverse

from movie_app.forms import SearchPersonForm


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
    data = {'first_name':'1',
            'last_name':'1',
            'year':1}
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
    url = reverse('detail_producer', kwargs={'id':p.id})
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['producer'] == p



