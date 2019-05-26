from django.forms.models import ModelForm
from django import forms
from .models import Movie


class MovieForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.field in ['title', 'french_title', 'genres', 'format', 'langue', 'localisation']:
                visible.field.required = True
            else:
                visible.field.required = False

    class Meta:
        model = Movie
        fields = ('title','french_title', 'synopsis', 'genres', 'date', 'actors', 'realisators', 'format', 'langue', 'localisation')
        widgets = {
            'actors': forms.SelectMultiple,
            'realisators': forms.SelectMultiple,
            'genres': forms.SelectMultiple,
        }


class MovieListForm(ModelForm):
    search_field = forms.CharField(max_length=250)
