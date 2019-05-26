from django.db import models
from common.models import Genre, Person, Localisation

# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=300, help_text='Nom du jeu', unique=True)
    description = models.TextField(help_text='description du jeu')
    genres = models.ManyToManyField(Genre, help_text='genres du jeu')
    date = models.DateTimeField()
    creators = models.ManyToManyField(Person, help_text='createurs du jeu', related_name='creators')
    tarif = models.FloatField(null=True)
    localisation = models.ForeignKey(Localisation, help_text="lieu où est le film", on_delete=models.DO_NOTHING)
    playersmin = models.IntegerField(help_text='Nombre de joueurs minimum')
    playersmax = models.IntegerField(help_text='Nombre de joueurs maximum')
    timemin = models.IntegerField(null=True, help_text='temps de jeu minimum')
    timemax = models.IntegerField(null=True, help_text='temps de jeu maximum')
    agemin = models.IntegerField(null=True, help_text='age minimum')
    extension = models.BooleanField(default=False, help_text="Est ce que ce jeu est une extension d'un autre?")


    def __str__(self):
        return self.title
