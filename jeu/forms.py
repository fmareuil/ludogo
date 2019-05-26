from django.forms.models import ModelForm
from django import forms
from .models import Game


class GameForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.field in ['title', 'genres', 'localisation']:
                visible.field.required = True
            else:
                visible.field.required = False

    class Meta:
        model = Game
        fields = ('title', 'description', 'genres', 'date', 'creators', 'tarif', 'localisation')
        widgets = {
            'creators': forms.SelectMultiple,
        }


class GameListForm(ModelForm):
    search_field = forms.CharField(max_length=250)
