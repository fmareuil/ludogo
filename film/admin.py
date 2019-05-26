# coding=utf-8
from django.contrib import admin
from .models import Movie, Format, Langue


# Register your models here.
admin.site.register(Movie)
admin.site.register(Format)
admin.site.register(Langue)