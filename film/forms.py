# coding=utf-8
from django.forms.models import ModelForm
from django import forms
from .models import Movie
from common.models import Genre


class MovieForm(ModelForm):

    date = forms.DateField(
        widget=forms.DateInput(format='%Y', attrs={'class': 'datepicker'}),
        input_formats=('%Y',)
    )

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.field in ['title', 'french_title', 'genres', 'format', 'langue', 'localisation']:
                visible.field.required = True
            else:
                visible.field.required = False
        self.fields['genres'].queryset = Genre.objects.filter(type=Genre.TYPE_MOVIE)

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
