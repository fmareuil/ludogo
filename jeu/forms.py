from django.forms.models import ModelForm
from django import forms
from .models import Game
from common.models import Genre, Person


class GameForm(ModelForm):

    date = forms.DateField(
        widget=forms.DateInput(format='%Y', attrs={'class': 'datepicker'}),
        input_formats=('%Y',)
    )

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.label in ['Extension']:
                visible.field.widget.attrs['class'] = ''
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.field.label in ['Title', 'Genres', 'Localisation', 'Playersmin', 'Playersmax', 'Creators',
                                       'Date']:
                visible.field.required = True
            else:
                visible.field.required = False
            if visible.field.label in ['Creators','Genres']:
                visible.field.widget.attrs['size'] = 10
        self.fields['genres'].queryset = Genre.objects.filter(type=Genre.TYPE_GAME)
        self.fields['creators'].queryset = Person.objects.all().order_by('firstname')

    class Meta:
        model = Game
        fields = ('title', 'description', 'genres', 'date', 'creators', 'tarif', 'localisation', 'playersmin',
                  'playersmax', 'timemin', 'timemax', 'agemin', 'extension')
        widgets = {
            'creators': forms.SelectMultiple,
        }


class GameListForm(ModelForm):
    search_field = forms.CharField(max_length=250)
