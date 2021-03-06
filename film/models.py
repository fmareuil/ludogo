# coding=utf-8
from django.db import models
from common.models import Genre, Person, Localisation

# Create your models here.


class Format(models.Model):
    name = models.CharField(max_length=100, help_text='Nom du format', unique=True)
    description = models.CharField(max_length=100, help_text='Rapide description du format', blank=True)

    def __str__(self):
        return self.name


class Langue(models.Model):
    name = models.CharField(max_length=100, help_text='Nom du format', unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    TT_PUBLIC = "tous publics"
    TT_PUBLICW = "tous publics (avec avertissement)"
    DIX = "10"
    DOUZE = "12"
    SEIZE = "16"
    DIXHUIT = "18"
    X = "X"
    TYPE_CERTIF = ((TT_PUBLIC, 'Tous publics'), (TT_PUBLICW, 'Tous publics (avec avertissement)'), (DIX, 'plus de 10ans'),
                   (DOUZE,'plus de 12ans'), (SEIZE, 'plus de 16ans'), (DIXHUIT, 'plus de 18ans'), (X, 'Adulte'))
    title = models.CharField(max_length=300, help_text='Titre du film original')
    french_title = models.CharField(max_length=300, help_text='Titre du film français')
    synopsis = models.TextField(help_text='synopsis du film')
    genres = models.ManyToManyField(Genre, help_text='genres du film')
    date = models.DateTimeField()
    actors = models.ManyToManyField(Person, help_text='acteurs principaux du film', related_name='actors')
    realisators = models.ManyToManyField(Person, help_text='realisateurs du film', related_name='realisators')
    format = models.ForeignKey(Format, help_text="format du film", on_delete=models.DO_NOTHING)
    langue = models.ForeignKey(Langue, help_text="langue.s du film", on_delete=models.DO_NOTHING)
    localisation = models.ForeignKey(Localisation, help_text="lieu où est le film", on_delete=models.DO_NOTHING)
    certificate = models.CharField(max_length=50, help_text='certification', choices=TYPE_CERTIF)

    class Meta:
        unique_together = ['title', 'format', 'langue']

    def __str__(self):
        return self.title
