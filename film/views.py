# coding=utf-8
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from .models import Movie
from .forms import MovieForm, MovieListForm
from common.models import Genre, Person
from django.urls import reverse_lazy

import imdb
import datetime

# Create your views here.


class MovieDetailView(generic.DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'


class MovieUpdateView(generic.UpdateView):
    model = Movie
    form_class = MovieForm
    pk_url_kwarg = 'movie_id'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("film:detail")

    def get_success_url(self):
        return reverse_lazy('film:detail', kwargs=self.kwargs)


class MovieCreateView(generic.CreateView):
    model = Movie
    form_class = MovieForm
    template_name_suffix = '_update_form'

    def get_initial(self):
        ia = imdb.IMDb()
        movie = ia.get_movie(self.kwargs['imdb_id'])
        fraka = get_aka(movie['aka'][0])
        newmovie = {}
        if 'synopsis' in movie:
            newmovie['synopsis'] = movie['synopsis'][0]
        if 'title' in movie:
            newmovie['title'] = movie['title']
        if 'year' in movie:
            newmovie['date'] = datetime.datetime(movie['year'], 1, 1)

        if fraka:
            newmovie['french_title'] = fraka
        listg = []
        if not 'genres' in movie:
            movie['genres'] = []
        for genre in movie['genres']:
            g = Genre.objects.get_or_create(type=Genre.TYPE_MOVIE, name=genre)
            listg.append(g[0].id)
        newmovie['genres'] = listg
        if 'cast' in movie:
            listact = []
            for actor in movie['cast']:
                name = actor['long imdb canonical name'].split(',')
                ac = Person.objects.get_or_create(firstname=name[1], lastname=name[0])
                listact.append(ac[0].id)
            newmovie['actors'] = listact
        listreal = []
        if not 'directors' in movie:
            movie['directors'] = []
        for realisator in movie['directors']:
            realname = realisator['long imdb canonical name'].split(',')
            real = Person.objects.get_or_create(firstname=realname[1], lastname=realname[0])
            listreal.append(real[0].id)
        newmovie['realisators'] = listreal
        return newmovie

    def get_success_url(self):
        return reverse_lazy('film:detail', kwargs={'movie_id':self.object.pk})


def searchmovie(request):
    if request.method == "GET":
        ia = imdb.IMDb()
        newmovie = request.GET.get('newmovie', None)
        if newmovie:
            result = ia.search_movie(newmovie)
        else:
            result = []
        movies = []
        for movie in result:
            if movie['kind'] == 'movie':
                if 'aka' in movie:
                    dic_movie = {'imdb_title': movie['long imdb canonical title'],
                                 'title': movie['title'],
                                 'year': movie['year'],
                                 'aka': movie['aka'],
                                 'movieID': movie.movieID}
                else:
                    dic_movie = {'imdb_title': movie['long imdb canonical title'],
                                 'title': movie['title'],
                                 'year': movie['year'],
                                 'movieID': movie.movieID}
                movies.append(dic_movie)
        return render(request, 'film/addnew_movie.html', {'movies': movies})
    elif request.method == "POST":
           return redirect(reverse_lazy('film:create', kwargs={'imdb_id':request.POST['movie']}))
    else:
        return render(request, 'film/addnew_movie.html')

def get_aka(aka):
    import re
    akas = re.sub(' +',' ', aka).split('\n \n \n')
    for aka in akas:
        if 'France' in aka:
            fr_aka = aka.split('\n')[0]
        else:
            fr_aka = ""
    return str(fr_aka.strip())

class MovieListView(generic.ListView):
    model = Movie
    form_class = MovieListForm
    template_name = 'film/search_movie.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView,self).get_context_data(**kwargs)
        context['view_search_field'] = self.request.GET.get('search_field',None)
        return context

    def get_queryset(self):
        pattern = self.request.GET.get('search_field',None)
        if pattern:
            object_list = self.model.objects.filter(Q(title__icontains=pattern) |
                                                    Q(actors__firstname__icontains=pattern) |
                                                    Q(actors__lastname__icontains=pattern) |
                                                    Q(genres__name__icontains=pattern) |
                                                    Q(french_title__icontains=pattern) |
                                                    Q(realisators__firstname__icontains=pattern) |
                                                    Q(realisators__firstname__icontains=pattern)).distinct()
        else:
            object_list = []
        return object_list


class MovieDeleteView(generic.DeleteView):
    model = Movie
    template_name = 'common/confirm_delete.html'
    pk_url_kwarg = 'movie_id'

    def get_success_url(self):
        return reverse_lazy('film:search')
