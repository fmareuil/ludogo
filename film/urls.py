# coding=utf-8
from django.urls import path
from .views import MovieDetailView, MovieUpdateView, MovieCreateView, searchmovie, MovieListView, MovieDeleteView

app_name = 'film'
urlpatterns = [
    path(r'addnew', searchmovie, name="addnew"),
    path(r'search', MovieListView.as_view(), name="search"),
    path(r'addnew/<slug:imdb_id>', MovieCreateView.as_view(), name="create"),
    path(r'<int:movie_id>', MovieDetailView.as_view(), name="detail"),
    path(r'update/<int:movie_id>', MovieUpdateView.as_view(), name="update"),
    path(r'delete/<int:movie_id>', MovieDeleteView.as_view(), name="delete"),
]