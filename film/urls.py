from django.conf.urls import include, url
from .views import MovieDetailView

app_name = 'film'
urlpatterns = [
    url(r'^(?P<movie_id>\d+)$', MovieDetailView.as_view(), name="detail"),
]