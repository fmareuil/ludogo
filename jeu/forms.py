from django.forms.models import ModelForm
from django import forms
from .models import Game
from common.models import Genre

class GameForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.label in ['Extension']:
                visible.field.widget.attrs['class'] = ''
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.field.label in ['Title', 'Genres', 'Localisation', 'Playersmin', 'Playersmax', 'Creators']:
                visible.field.required = True
            else:
                visible.field.required = False
        self.fields['genres'].queryset = Genre.objects.filter(type=Genre.TYPE_GAME)

    class Meta:
        model = Game
        fields = ('title', 'description', 'genres', 'date', 'creators', 'tarif', 'localisation', 'playersmin',
                  'playersmax', 'timemin', 'timemax', 'agemin', 'extension')
        widgets = {
            'creators': forms.SelectMultiple,
        }


class GameListForm(ModelForm):
    search_field = forms.CharField(max_length=250)
