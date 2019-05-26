from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from .models import Game
from .forms import GameForm, GameListForm
from common.models import Genre, Person
from django.urls import reverse_lazy
import requests

import imdb
import datetime
URL_REQUEST = 'https://www.tabletopfinder.eu/query/boardgames/search'
# Create your views here.


class GameDetailView(generic.DetailView):
    model = Game
    pk_url_kwarg = 'game_id'


class GameUpdateView(generic.UpdateView):
    model = Game
    form_class = GameForm
    pk_url_kwarg = 'Game_id'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("jeu:detail")

    def get_success_url(self):
        return reverse_lazy('jeu:detail', kwargs=self.kwargs)


class GameCreateView(generic.CreateView):
    model = Game
    form_class = GameForm
    template_name_suffix = '_update_form'

    def get_initial(self):
        return super(GameCreateView, self).get_initial()

    def get_success_url(self):
        return reverse_lazy('jeu:detail', kwargs={'game_id':self.object.pk})


def searchgame(request):
    if request.method == "GET":
        newgame = request.GET.get('newgame', None)
        if newgame:
            payload = {'query': newgame}
            result = requests.get(URL_REQUEST, params=payload)
            print(result.url)
            result = result.json()
        else:
            result = {'games':[]}
        games = []
        for game in result['games']:
            games.append({'title':game['name'],
                          'gameID':game['id']})
        return render(request, 'jeu/addnew_game.html', {'games': games})
    elif request.method == "POST":
           return redirect(reverse_lazy('jeu:create', kwargs={'ttf_id':request.POST['game']}))
    else:
        return render(request, 'jeu/addnew_game.html')


class GameListView(generic.ListView):
    model = Game
    form_class = GameListForm
    template_name = 'jeu/search_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GameListView,self).get_context_data(**kwargs)
        context['view_search_field'] = self.request.GET.get('search_field',None)
        return context

    def get_queryset(self):
        pattern = self.request.GET.get('search_field',None)
        if pattern:
            object_list = self.model.objects.filter(Q(title__icontains=pattern) |
                                                    Q(creators__firstname__icontains=pattern) |
                                                    Q(creators__lastname__icontains=pattern) |
                                                    Q(genres__name__icontains=pattern)).distinct()
        else:
            object_list = []
        return object_list


class GameDeleteView(generic.DeleteView):
    model = Game
    template_name = 'common/confirm_delete.html'
    pk_url_kwarg = 'game_id'

    def get_success_url(self):
        return reverse_lazy('jeu:search')
