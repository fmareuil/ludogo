from django.forms.models import ModelForm
from .models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'synopsis', 'genres', 'date', 'actors', 'realisators', 'format', 'langue', 'localisation')