from django.shortcuts import render
from django.views import generic
from .models import Movie
from .forms import MovieForm

# Create your views here.

class MovieDetailView(generic.DetailView):
    model = Movie
    form_class = MovieForm
    pk_url_kwarg = 'movie_id'
