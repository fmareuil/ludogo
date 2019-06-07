# coding=utf-8
from django.forms.models import ModelForm
from django import forms
from .models import Movie
from common.models import Genre, Person


class MovieForm(ModelForm):
    note = forms.CharField(max_length=150)
    certificates = forms.CharField(max_length=300)
    date = forms.DateField(
        widget=forms.DateInput(format='%Y', attrs={'class': 'datepicker'}),
        input_formats=('%Y',)
    )

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.field.label in ['Title', 'French_title', 'Genres', 'Format', 'Langue', 'Localisation', 'Date',
                                       'Certificate']:
                visible.field.required = True
            else:
                visible.field.required = False
            if visible.field.label in ['Actors', 'Realisators', 'Genres']:
                visible.field.widget.attrs['size'] = 10
        self.fields['genres'].queryset = Genre.objects.filter(type=Genre.TYPE_MOVIE)
        self.fields['actors'].queryset = Person.objects.all().order_by('firstname')
        self.fields['realisators'].queryset = Person.objects.all().order_by('firstname')

    class Meta:
        model = Movie
        fields = ('title','french_title', 'synopsis', 'genres', 'date', 'actors', 'realisators', 'format', 'langue',
                  'localisation', 'certificate')
        widgets = {
            'actors': forms.SelectMultiple,
            'realisators': forms.SelectMultiple,
            'genres': forms.SelectMultiple,
        }


class MovieListForm(ModelForm):
    search_field = forms.CharField(max_length=250)
