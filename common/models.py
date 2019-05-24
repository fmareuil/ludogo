from django.db import models

# Create your models here.


class Genre(models.Model):
    TYPE_MOVIE = 'film'
    TYPE_GAME = 'jeu'
    TYPE_CHOICES = ((TYPE_MOVIE, 'film'), (TYPE_GAME, 'jeu'))
    name = models.CharField(max_length=100, help_text='Nom du genre')
    type = models.CharField(max_length=100, help_text='Type du genre', choices=TYPE_CHOICES)
    description = models.CharField(max_length=150, help_text='Une courte description du genre', blank=True)

    class Meta:
        unique_together = ['name', 'type']


class Person(models.Model):
    firstname = models.CharField(max_length=100, help_text='Prenom')
    lastname = models.CharField(max_length=100, help_text='Nom de Famille')


    class Meta:
        unique_together = ['firstname', 'lastname']


class Localisation(models.Model):
    name = models.CharField(max_length=100, help_text='Nom du lieu')
    details = models.CharField(max_length=100, help_text="details de l'emplacement")

    class Meta:
        unique_together = ['name', 'details']
