# coding=utf-8
from django.contrib import admin
from .models import Person, Localisation, Genre
from film.models import Movie
from jeu.models import Game
from django.db.models import Q
# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    actions = ['clean_persons']

    def clean_persons(self, request, queryset):
        for person in queryset:
            listmovies = Movie.objects.filter(Q(actors__id=person.id) | Q(realisators__id=person.id))
            if not listmovies:
                listgames = Game.objects.filter(creators__id=person.id)
                if not listgames:
                    person.delete()


# Register your models here.
admin.site.register(Person, PersonAdmin)
admin.site.register(Localisation)
admin.site.register(Genre)
