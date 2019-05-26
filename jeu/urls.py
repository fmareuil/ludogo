from django.conf.urls import url
from .views import searchgame, GameListView, GameDetailView, GameDeleteView, GameUpdateView, GameCreateView

app_name = 'jeu'
urlpatterns = [
    url(r'^addnew$', searchgame, name="addnew"),
    url(r'^search$', GameListView.as_view(), name="search"),
    url(r'^addnew/(?P<imdb_id>\d+)$', GameCreateView.as_view(), name="create"),
    url(r'^(?P<movie_id>\d+)$', GameDetailView.as_view(), name="detail"),
    url(r'^update/(?P<movie_id>\d+)$', GameUpdateView.as_view(), name="update"),
    url(r'^delete/(?P<movie_id>\d+)$', GameDeleteView.as_view(), name="delete"),
]