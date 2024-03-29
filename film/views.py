# coding=utf-8
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q, Count
from .models import Movie
from .forms import MovieForm, MovieListForm
from common.models import Genre, Person
from django.urls import reverse_lazy
from collections import Counter

from imdb import Cinemagoer
import datetime
import random as rand
import re

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
        if self.kwargs['imdb_id'] != 'empty':
            ia = Cinemagoer()
            movie = ia.get_movie(self.kwargs['imdb_id'])
            fraka = get_aka(movie['aka'][0])
            newmovie = {}
            if 'synopsis' in movie:
                newmovie['synopsis'] = movie['synopsis'][0]
            elif 'plot outline' in movie:
                newmovie['synopsis'] = movie['plot outline']
            elif 'plot' in movie:
                newmovie['synopsis'] = movie['plot'][0].split('::')[0]
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
                for actor in movie['cast'][0:6]:
                    name = actor['long imdb canonical name'].split(',')
                    if len(name) > 1:
                        ac = Person.objects.get_or_create(firstname=name[1], lastname=name[0])
                    else:
                        ac = Person.objects.get_or_create(firstname='', lastname=name[0])
                    listact.append(ac[0].id)
                newmovie['actors'] = listact
            listreal = []
            if not 'directors' in movie:
                movie['directors'] = []
            for realisator in movie['directors']:
                realname = realisator['long imdb canonical name'].split(',')
                if len(realname) > 1:
                    real = Person.objects.get_or_create(firstname=realname[1], lastname=realname[0])
                else:
                    real = Person.objects.get_or_create(firstname='', lastname=realname[0])
                listreal.append(real[0].id)
            newmovie['realisators'] = listreal
            if 'certificates' in movie:
                for certif in movie['certificates']:
                    if 'France' in certif:
                        newmovie['certificate'] = certif.split(':')[1].lower()
                if not 'certificate' in newmovie:
                    newmovie['certificates'] = ', '.join(movie['certificates'])
            if 'rating' in movie:
                newmovie['note'] = movie['rating']
        else:
            newmovie = {}
        return newmovie

    def get_success_url(self):
        return reverse_lazy('film:detail', kwargs={'movie_id':self.object.pk})


def searchmovie(request):
    if request.method == "GET":
        ia = Cinemagoer()
        newmovie = request.GET.get('newmovie', None)
        if newmovie:
            result = ia.search_movie(newmovie)
        else:
            result = []
        movies = []
        for movie in result:
            if movie['kind'] == 'movie':
                dic_movie = {}
                if 'aka' in movie.keys():
                    dic_movie['aka'] = movie['aka']
                if 'long imdb canonical title' in movie.keys():
                    dic_movie['imdb_title'] = movie['long imdb canonical title']
                if 'title' in movie.keys():
                    dic_movie['title'] = movie['title']
                if 'year' in movie.keys():
                    dic_movie['year'] = movie['year']
                dic_movie['movieID'] = movie.movieID
                movies.append(dic_movie)
        return render(request, 'film/addnew_movie.html', {'movies': movies})
    elif request.method == "POST":
        if 'movie' in request.POST:
            return redirect(reverse_lazy('film:create', kwargs={'imdb_id':request.POST['movie']}))
        else:
            return redirect(reverse_lazy('film:create', kwargs={'imdb_id': 'empty'}))
    else:
        return render(request, 'film/addnew_movie.html')

def get_aka(aka):
    akas = re.sub(' +',' ', aka).split('\n \n \n')
    fr_aka = ""
    for aka in akas:
        if 'France' in aka:
            fr_aka = str(aka.split('\n')[0].strip())
    return fr_aka


class MovieListView(generic.ListView):
    model = Movie
    form_class = MovieListForm
    template_name = 'film/search_movie.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView,self).get_context_data(**kwargs)
        searchfield = self.request.GET.get('search_field',None)
        searchactors = self.request.GET.get('search_actors',None)
        searchrealisators = self.request.GET.get('search_realisators',None)
        if searchfield or searchactors or searchrealisators:
            context['view_search_field'] = ' '.join([searchfield, searchactors, searchrealisators])
        context['nbr_movies'] = self.model.objects.count()
        return context

    def search_patterns(self, pattern, object_list):
        patterns = pattern.split()
        for pat in patterns:
            olist = self.model.objects.filter(Q(title__icontains=pat.strip()) |
                                              Q(french_title__icontains=pat.strip()) |
                                              Q(genres__name__icontains=pat.strip()))
            object_list = object_list.union(olist, all=True)
        return object_list

    def search_actors(self, pattern, object_list):
        patterns = pattern.split()
        for pat in patterns:
            olist = self.model.objects.filter(Q(actors__firstname__icontains=pat.strip()) |
                                              Q(actors__lastname__icontains=pat.strip()))
            object_list = object_list.union(olist, all=True)
        return object_list

    def search_realisators(self, pattern, object_list):
        patterns = pattern.split()
        for pat in patterns:
            olist = self.model.objects.filter(Q(realisators__firstname__icontains=pat.strip()) |
                                              Q(realisators__lastname__icontains=pat.strip()))
            object_list = object_list.union(olist, all=True)
        return object_list

    def get_queryset(self):
        pattern = self.request.GET.get('search_field',None)
        actor_pattern = self.request.GET.get('search_actors',None)
        realisator_pattern = self.request.GET.get('search_realisators',None)
        random = self.request.GET.get('random',None)
        object_list = self.model.objects.none()
        if pattern:
            object_list = self.search_patterns(pattern, object_list)
        if actor_pattern:
            object_list = self.search_actors(actor_pattern, object_list)
        if realisator_pattern:
            object_list = self.search_realisators(realisator_pattern, object_list)
        if random == 'yes':
            l = list(self.model.objects.values_list('id', flat=True))
            if len(l) > 0:
                olist = self.model.objects.filter(id=rand.choice(l))
                object_list = object_list.union(olist, all=True)
        result = [item for items, c in Counter(list(object_list.values_list('id', flat=True))).most_common()
                  for item in [items] * c]
        uniqresult = []
        for n in result:
            if not n in uniqresult:
                uniqresult.append(n)
        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(uniqresult)])
        ordering = 'CASE %s END' % clauses
        queryset = self.model.objects.filter(pk__in=uniqresult).extra(
            select={'ordering': ordering}, order_by=('ordering',))
        return queryset


class MovieDeleteView(generic.DeleteView):
    model = Movie
    template_name = 'common/confirm_delete.html'
    pk_url_kwarg = 'movie_id'

    def get_success_url(self):
        return reverse_lazy('film:search')
