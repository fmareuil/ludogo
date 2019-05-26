from django.db import models
from common.models import Genre, Person, Localisation

# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=300, help_text='Nom du jeu', unique=True)
    description = models.TextField(help_text='description du jeu')
    genres = models.ManyToManyField(Genre, help_text='genres du jeu')
    date = models.DateTimeField()
    creators = models.ManyToManyField(Person, help_text='createurs du jeu', related_name='creators')
    tarif = models.FloatField()
    localisation = models.ForeignKey(Localisation, help_text="lieu où est le film", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Extension(models.Model):
    game = models.ForeignKey(Game, help_text="Jeu d'origine", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text="Nom de l'extension")
    description = models.CharField(max_length=100, help_text="description de l'extension", blank=True)

    def __str__(self):
        return self.title
