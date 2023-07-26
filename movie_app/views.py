from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from movie_app.forms import AddPersonForm, AddProducderForm, AddMovieModelForm, SearchPersonForm, AddCommentToMovieForm
from movie_app.models import Genre, Person, Producer, Movie, Comment


class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


# Create your views here.

class AddGenreView(View):

    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):
        name = request.POST.get('name')
        Genre.objects.create(name=name)
        return redirect('add_genre')


class GenreListView(View):

    def get(self, request):
        genres = Genre.objects.all()
        return render(request, 'list_view.html', {'genres': genres})


class GenreAPIListView(View):

    def get(self, request):
        name = request.GET.get('name', '')
        genres = Genre.objects.filter(name__icontains=name)
        d = []
        for g in genres:
            d.append({'id': g.id, 'name': g.name})
        # d = [{'id':g.id, 'name':g.name} for g in genres]
        return JsonResponse(d, safe=False)


class AddPersonView(View):

    def get(self, request):
        form = AddPersonForm()
        return render(request, 'form2.html', {'form': form})

    def post(self, request):
        form = AddPersonForm(request.POST)
        if form.is_valid():
            Person.objects.create(
                **form.cleaned_data)
            return redirect('add_person')
        return render(request, 'form2.html', {'form': form})


class AddProducerView(View):

    def get(self, request):
        form = AddProducderForm()
        return render(request, 'form2.html', {'form': form})

    def post(self, request):
        form = AddProducderForm(request.POST)
        if form.is_valid():
            Producer.objects.create(
                **form.cleaned_data)
            return redirect('add_producer')
        return render(request, 'form2.html', {'form': form})


class AddMovieView(View):

    def get(self, request):
        form = AddMovieModelForm()
        return render(request, 'form2.html', {'form': form})

    def post(self, request):
        form = AddMovieModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_movie')
        return render(request, 'form2.html', {'form': form})


class PersonListView(View):
    def get(self, request):
        persons = Person.objects.all()
        form = SearchPersonForm(request.GET)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            year = form.cleaned_data.get('year')
            persons = persons.filter(first_name__icontains=first_name, last_name__icontains=last_name)
            if year is not None:
                persons = persons.filter(year=year)
        return render(request, 'person_list.html', {'persons': persons, 'form': form})


class MovieListView(View):

    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movie_list.html', {'movies': movies})


class ProducerListView(View):

    def get(self, request):
        producers = Movie.objects.all()
        return render(request, 'producer_list.html', {'producers': producers})


class ProducerDetailView(View):

    def get(self, request, id):
        producer = Producer.objects.get(pk=id)
        return render(request, 'producer_detail.html', {'producer': producer})


class ProducerGenericDetailView(DetailView):
    model = Producer
    template_name = 'producer_detail.html'


class ProducerGenericUpdateView(UpdateView):
    model = Producer
    template_name = 'form2.html'
    fields = '__all__'
    success_url = reverse_lazy('detail_genreric_producer')


class ProducerGenericCreateView(CreateView):
    model = Producer
    template_name = 'form2.html'
    fields = '__all__'
    success_url = reverse_lazy('detail_genreric_producer')


class ProducerGenericListView(ListView):
    model = Producer
    template_name = 'producer_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):  # przykład jak rozszerzyć kontekst o dodatkowe zmienne
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['msg'] = "boli mnie bark"
        return context


class PersonDetailView(View):

    def get(self, request, id):
        person = Person.objects.get(pk=id)
        return render(request, 'person_detail.html', {'person': person, 'dupa': 'ala ma kota'})


class MovieDetailView(View):

    def get(self, request, id):
        movie = Movie.objects.get(pk=id)
        return render(request, 'movie_detail.html', {'movie': movie})


class GenreDetailView(PermissionRequiredMixin, View):
    permission_required = ['movie_app.view_genre']

    def get(self, request, id):
        genre = Genre.objects.get(pk=id)
        return render(request, 'genre_detail.html', {'genre': genre})


class AddCommentToMovieView(LoginRequiredMixin, View):

    def get(self, request, id_movie):
        form = AddCommentToMovieForm()
        return render(request, 'form2.html', {'form': form})

    def post(self, request, id_movie):
        form = AddCommentToMovieForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = Movie.objects.get(pk=id_movie)
            comment.creator = request.user
            comment.save()
            return redirect('detail_movie', id_movie)
        return render(request, 'form2.html', {'form': form})


class UpdateCommentView(UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'form2.html'
    fields = ['text']

    def test_func(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        return comment.creator == self.request.user

    def get_success_url(self):
        return reverse('detail_movie', kwargs={'id': self.object.movie.pk})
