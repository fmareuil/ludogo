from django.conf.urls import include, url
from .views import MovieDetailView, MovieUpdateView, MovieCreateView, searchmovie, MovieListView, MovieDeleteView

app_name = 'film'
urlpatterns = [
    url(r'^addnew$', searchmovie, name="addnew"),
    url(r'^search$', MovieListView.as_view(), name="search"),
    url(r'^addnew/(?P<imdb_id>\d+)$', MovieCreateView.as_view(), name="create"),
    url(r'^(?P<movie_id>\d+)$', MovieDetailView.as_view(), name="detail"),
    url(r'^update/(?P<movie_id>\d+)$', MovieUpdateView.as_view(), name="update"),
    url(r'^delete/(?P<movie_id>\d+)$', MovieDeleteView.as_view(), name="delete"),
]