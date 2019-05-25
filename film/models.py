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
    title = models.CharField(max_length=300, help_text='Titre du film')
    synopsis = models.TextField(help_text='synopsis du film')
    genres = models.ManyToManyField(Genre, help_text='genres du film')
    date = models.DateTimeField()
    actors = models.ManyToManyField(Person, help_text='acteurs principaux du film', related_name='actors')
    realisators = models.ManyToManyField(Person, help_text='realisateurs du film', related_name='realisators')
    format = models.ForeignKey(Format, help_text="format du film", on_delete=models.DO_NOTHING)
    langue = models.ForeignKey(Langue, help_text="langue.s du film", on_delete=models.DO_NOTHING)
    localisation = models.ForeignKey(Localisation, help_text="lieu où est le film", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['title', 'format', 'langue']

    def __str__(self):
        return self.title