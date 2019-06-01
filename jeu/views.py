# coding=utf-8
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q, Sum
from .models import Game
from .forms import GameForm, GameListForm
from common.models import Person
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
import requests
import datetime

URL_REQUEST_TTF = 'https://www.tabletopfinder.eu/query/boardgames/search'
URL_HTML_TTF = 'https://www.tabletopfinder.eu/fr/boardgame/{}/'

URL_REQUEST_TRICTRAC = 'https://www.trictrac.net/recherche'
URL_HTML_TRICTRAC = 'https://www.trictrac.net/jeu-de-societe/{}'
# Create your views here.


class GameDetailView(generic.DetailView):
    model = Game
    pk_url_kwarg = 'game_id'


class GameUpdateView(generic.UpdateView):
    model = Game
    form_class = GameForm
    pk_url_kwarg = 'game_id'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("jeu:detail")

    def get_success_url(self):
        return reverse_lazy('jeu:detail', kwargs=self.kwargs)

def getfromttf(dbid):
    url = URL_HTML_TTF.format(dbid)
    htmlresult = requests.get(url)
    soupresult = BeautifulSoup(htmlresult.text)
    title = soupresult.find('h1')
    if title:
        title = title.text
    description = soupresult.find('div', attrs={"class": "description"})
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
    agemin = soupresult.find('i', attrs={"class": u"fas fa-child"})
    if agemin:
        agemin = int(agemin.parent.text.split('\n')[-2].split('+')[0])
    playersmin = None
    playersmax = None
    timemin = None
    timemax = None
    tarif = None
    pages = range(1, 10)
    exit = False
    for page in pages:
        payload = {'query': title.replace(' ', '+').lower(), 'page': page}
        results = requests.get(URL_REQUEST_TTF, params=payload)
        results = results.json()
        for result in results['games']:
            if result['id'] == int(dbid):
                playersmin = result['playersMin']
                playersmax = result['playersMax']
                timemin = result['timeMin']
                timemax = result['timeMax']
                tarif = result['price']
                exit = True
            if exit:
                break
        if exit:
            break
    urls = [url, "{}?query={}&page={}".format(URL_REQUEST_TTF, title.replace(' ', '+').lower(), page)]
    newgame = {'title': title, 'description': description, 'date': datetime.datetime(date, 1, 1),
               'creators': listcreat, 'agemin': agemin, 'playersmin': playersmin, 'playersmax': playersmax,
               'timemin': timemin, 'timemax': timemax, 'tarif': tarif}
    return newgame, urls

def getfromtrictrac(dbid):
    url = URL_HTML_TRICTRAC.format(dbid)
    htmlresult = requests.get(url)
    soupresult = BeautifulSoup(htmlresult.text)
    title = None
    description = None
    agemin = None
    playersmin = None
    playersmax = None
    timemin = None
    timemax = None
    tarif = None
    date = None
    listcreat = []
    title = soupresult.find('h1', attrs={"itemprop":"name"})
    if title:
        title = title.find_next('a').text.strip()

    psmall = soupresult.findAll('p', attrs={"class":"small"})
    for p in psmall:
        span = p.find_next('span').text
        if "édition" in span:
            date = span.strip("édition").strip()
        if 'Par ' in p:
            aref = p.find_all('a')
    par = 0
    for a in aref:
        if 'Par' in a.previous:
            par=1
            name = a.text.strip().split()
            creat = Person.objects.get_or_create(firstname=' '.join(name[0:-1]), lastname=name[-1])
            listcreat.append(creat[0].id)
        if ',' in a.previous and par:
            name = a.text.strip().split()
            creat = Person.objects.get_or_create(firstname=' '.join(name[0:-1]), lastname=name[-1])
            listcreat.append(creat[0].id)
        if 'et' in a.previous and par:
            name = a.text.strip().split()
            creat = Person.objects.get_or_create(firstname=' '.join(name[0:-1]), lastname=name[-1])
            listcreat.append(creat[0].id)
            break
    strongs = soupresult.findAll('strong')
    if strongs:
        for stro in strongs:
            if stro.text == 'Description du jeu':
                description = stro.find_next('p', attrs={"class":"readmore"}).text.strip('\n').strip()
            elif stro.text == 'Game play':
                agemintemp = stro.find_next('i', attrs={'class':'ion-ios-body-outline'})
                print(agemintemp.next, "AGEMIN")
                if agemintemp and agemintemp.next:
                    agemintemp = agemintemp.next.lower()
                    if "à partir de" in agemintemp:
                        agemin = agemintemp.strip('à partir de').strip('ans').strip()
                players = stro.find_next('i', attrs={"class":"ion-ios-people-outline"})
                if players and players.next:
                    players = players.next.lower()
                    if "jusqu'à" in players:
                        playersmin = players.strip("jusqu'à").strip("joueurs").strip()
                        playersmax = playersmin
                    else:
                        players = players.split('à')
                        playersmin = players[0].strip()
                        playersmax = players[1].strip()
                timemintemp = stro.find_next('i', attrs={'class':'ion-ios-timer-outline'})
                if timemintemp and timemintemp.next:
                    timemintemp = timemintemp.next.lower()
                    timemin = timemintemp.strip('min').strip()
                    timemax = timemin
            elif stro.text == "Prix public conseillé":
                if stro.next:
                    tarif = stro.next.next.lower().strip(': ').strip('€').strip().replace(',','.')
    urls = [url, "{}?query={}&limite=20".format(URL_REQUEST_TRICTRAC, dbid)]
    newgame = {'title': title, 'description': description, 'date': datetime.datetime(int(date), 1, 1),
               'creators': listcreat, 'agemin': agemin, 'playersmin': playersmin, 'playersmax': playersmax,
               'timemin': timemin, 'timemax': timemax, 'tarif': tarif}
    return newgame, urls


class GameCreateView(generic.CreateView):
    model = Game
    form_class = GameForm
    template_name_suffix = '_update_form'

    def get_initial(self):
        #TODO: delete old messages
        #storage = messages.get_messages(self.request)
        #storage.used = True
        #if len(storage._loaded_messages) == 3: 
        #    del storage._loaded_messages[0]
        #    del storage._loaded_messages[1]
        #    del storage._loaded_messages[2]
        if self.kwargs['db_id'] != 'empty':
            if self.kwargs['dbsearch'] == 'ttf':
                newgame, urls = getfromttf(self.kwargs['db_id'])
                messages.add_message(self.request, messages.INFO, '{}'.format(urls[0]))
                messages.add_message(self.request, messages.INFO, '{}'.format(urls[1]))
            elif self.kwargs['dbsearch'] == 'trictrac':
                newgame, urls = getfromtrictrac(self.kwargs['db_id'])
                messages.add_message(self.request, messages.INFO, '{}'.format(urls[0]))
                messages.add_message(self.request, messages.INFO, '{}'.format(urls[1]))
            else:
                newgame = {}

        else:
            newgame = {}
        return newgame

    def get_success_url(self):
        return reverse_lazy('jeu:detail', kwargs={'game_id':self.object.pk})

def ttfsearch(query):
    payload = {'query': query.replace(' ', '+').lower(), 'page': 1}
    result = requests.get(URL_REQUEST_TTF, params=payload)
    result = result.json()
    payload = {'query': query.replace(' ', '+').lower(), 'page': 2}
    result2 = requests.get(URL_REQUEST_TTF, params=payload)
    result2 = result2.json()
    if result != result2:
        for r in result2['games']:
            result['games'].append(r)
    return result

def trictracsearch(query):
    payload = {'search':query, 'limit':20}
    htmlresult = requests.get(URL_REQUEST_TRICTRAC, params=payload)
    soupresult = BeautifulSoup(htmlresult.text)
    items = soupresult.find_all('div', attrs={"class": "item"})
    result = {}
    result['games'] = []
    for item in items:
        aref = item.find_next('a', attrs={"class":"header"})
        game = {'name':aref.text.strip(),'id':aref['href'].split('/')[-1]}
        result['games'].append(game)
    return result

def searchgame(request):
    if request.method == "GET":
        newgame = request.GET.get('newgame', None)
        dbsearch = request.GET.get('dbsearch', None)
        if newgame:
            if dbsearch == 'ttf':
                result = ttfsearch(newgame)
            elif dbsearch == 'trictrac':
                result = trictracsearch(newgame)
            else:
                result = {'games': []}

        else:
            result = {'games':[]}
        games = []
        for game in result['games']:
            games.append({'title':game['name'],
                          'gameID':game['id']})
        return render(request, 'jeu/addnew_game.html', {'games': games, 'dbsearch':dbsearch})
    elif request.method == "POST":
        if 'game' in request.POST:
           return redirect(reverse_lazy('jeu:create', kwargs={'db_id':request.POST['game'],
                                                              'dbsearch':request.POST['dbsearch']}))
        else:
           return redirect(reverse_lazy('jeu:create', kwargs={'db_id': 'empty',
                                                              'dbsearch':request.POST['dbsearch']}))
    else:
        return render(request, 'jeu/addnew_game.html')


class GameListView(generic.ListView):
    model = Game
    form_class = GameListForm
    template_name = 'jeu/search_game.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GameListView,self).get_context_data(**kwargs)
        context['view_search_field'] = self.request.GET.get('search_field',None)
        context['nbr_games'] = self.model.objects.count()
        context['valeur'] = self.model.objects.aggregate(Sum('tarif'))
        return context

    def get_queryset(self):
        pattern = self.request.GET.get('search_field',None)
        timetoplay = self.request.GET.get('max_time',None)
        nbplayer = self.request.GET.get('nb_play',None)
        object_list = self.model.objects.none()
        if pattern:
            patterns = pattern.split()
            for pat in patterns:
                olist = self.model.objects.filter(Q(title__icontains=pat) |
                                                 Q(creators__firstname__icontains=pat) |
                                                 Q(creators__lastname__icontains=pat) |
                                                 Q(genres__name__icontains=pat)).distinct()
            object_list = object_list | olist
        if timetoplay:
            olist = self.model.objects.filter(timemax__lte=int(timetoplay))
            if not object_list:
                object_list = olist
            else:
                object_list = object_list.intersection(olist)
        if nbplayer:
            olist = self.model.objects.filter(playersmax__gte=int(nbplayer), playersmin__lte=int(nbplayer))
            if not object_list:
                object_list = olist
            else:
                object_list = object_list.intersection(olist)
        return object_list


class GameDeleteView(generic.DeleteView):
    model = Game
    template_name = 'common/confirm_delete.html'
    pk_url_kwarg = 'game_id'

    def get_success_url(self):
        return reverse_lazy('jeu:search')
