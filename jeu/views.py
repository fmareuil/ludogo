from django.contrib import messages

# Create your views here.
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from .models import Game
from .forms import GameForm, GameListForm
from common.models import Genre, Person
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
import requests
import datetime

URL_REQUEST = 'https://www.tabletopfinder.eu/query/boardgames/search'
URL_HTML = 'https://www.tabletopfinder.eu/fr/boardgame/{}/'
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
        url = URL_HTML.format(self.kwargs['ttf_id'])
        htmlresult = requests.get(url)
        soupresult = BeautifulSoup(htmlresult.text)
        title = soupresult.find('h1')
        if title:
            title = title.text
        description = soupresult.find('div', attrs={"class":"description"})
        if description:
            description = description.text.strip('\n').strip('voir plus...')
        listcreat = []
        strongs = soupresult.findAll('strong')
        if not strongs:
            strongs = []
            date = None
        for stro in strongs:
            if stro.text == 'publié':
                lidates = stro.find_next('ul').find_all('li')
                date = int(lidates[0].text.strip('\n').strip())
            elif stro.text == 'concepteurs' or stro.text == 'designer' or stro.text == 'concepteur' \
                    or stro.text == 'designers':
                liconcepteurs = stro.find_next('ul').find_all('li')
                for concepteur in liconcepteurs:
                    name = concepteur.find('a').text.strip('\n').strip().split(' ')
                    creat = Person.objects.get_or_create(firstname=' '.join(name[0:-1]), lastname=name[-1])
                    listcreat.append(creat[0].id)
        agemin = soupresult.find('i', attrs={"class":u"fas fa-child"})
        if agemin:
            agemin = int(agemin.parent.text.split('\n')[-2].split('+')[0])
        payload = {'query': title}
        results = requests.get(URL_REQUEST, params=payload)
        results = results.json()
        playersmin = None
        playersmax = None
        timemin = None
        timemax = None
        tarif = None
        for result in results['games']:
            if result['id'] == int(self.kwargs['ttf_id']):
                playersmin = result['playersMin']
                playersmax = result['playersMax']
                timemin = result['timeMin']
                timemax = result['timeMax']
                tarif = result['price']
        urls = [url, "{}?query='{}'".format(URL_REQUEST, title)]
        newgame = {'title': title, 'description': description, 'date': datetime.datetime(date, 1, 1),
                   'creators':listcreat, 'agemin':agemin, 'playersmin':playersmin, 'playersmax':playersmax,
                   'timemin':timemin, 'timemax':timemax, 'tarif':tarif}
        messages.add_message(self.request, messages.INFO, "Pour plus d'information vous pouvez regarder :")
        messages.add_message(self.request, messages.INFO, '{}'.format(urls[0]))
        messages.add_message(self.request, messages.INFO, '{}'.format(urls[1]))
        return newgame

    def get_success_url(self):
        return reverse_lazy('jeu:detail', kwargs={'game_id':self.object.pk})


def searchgame(request):
    if request.method == "GET":
        newgame = request.GET.get('newgame', None)
        if newgame:
            payload = {'query': newgame}
            result = requests.get(URL_REQUEST, params=payload)
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
