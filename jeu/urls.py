# coding=utf-8
from django.urls import path
from .views import searchgame, GameListView, GameDetailView, GameDeleteView, GameUpdateView, GameCreateView

app_name = 'jeu'
urlpatterns = [
    path(r'addnew', searchgame, name="addnew"),
    path(r'search', GameListView.as_view(), name="search"),
    path(r'addnew/<slug:dbsearch>/<slug:db_id>', GameCreateView.as_view(), name="create"),
    path(r'<int:game_id>', GameDetailView.as_view(), name="detail"),
    path(r'update/<int:game_id>', GameUpdateView.as_view(), name="update"),
    path(r'delete/<int:game_id>', GameDeleteView.as_view(), name="delete"),
]
