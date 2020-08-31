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

URL_REQUEST_TTF = 'https://www.tabletopfinder.eu/fr/boardgame/search'
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
    header = soupresult.find('div', attrs={'id': 'product-detail-header'})
    details = soupresult.find('div', attrs={'id': 'product-detail-properties'})
    tarifs = soupresult.find('div', attrs={'id': 'product-detail-prices'})
    title = header.find_next('h1')
    if title:
        title = title.text
    description = header.find_next('p')
    if description:
        description = description.text

    tarif = None
    agemin = None
    date = None
    listcreat = []
    players = header.find_next('div', attrs={'title': 'joueurs', 'class': 'tag'})
    playersmin = players.text.split('-')[0].strip()
    if len(players.text.split('-')) > 1:
        playersmax = players.text.split('-')[1].strip()
    else:
        playersmax = playersmin
    times = header.find_next('div', attrs={'title': 'temps', 'class': 'tag'})
    timemax = times.text.split('-')[0].strip()
    if len(times.text.split('-')) > 1:
        timemin = times.text.split('-')[1].strip()
    else:
        timemin = timemax
    tables = details.findAll('tr')
    for tr in tables:
        if tr.find_next('th').text == "Publié:":
            date = int(tr.find_next('td').text)
        if tr.find_next('th').text == "Concepteurs:":
            liconcepteurs = tr.findAll('li')
            for concepteur in liconcepteurs:
                name = concepteur.find('a').text.strip('\n').strip().split(' ')
                creat = Person.objects.get_or_create(firstname=' '.join(name[0:-1]), lastname=name[-1])
                listcreat.append(creat[0].id)
    prix = tarifs.findAll('tr')
    for tr in prix:
        tds = tr.findAll('td')
        if len(tds) >= 3:
            if tds[2].text.strip():
                pricetd = tds[2]
                if pricetd.find('small'):
                    pricetd.find('small').decompose()
                if pricetd.text.strip():
                    tarif = pricetd.text.strip().split(u'\xa0')[1].strip()
        if tarif:
            break

    urls = [url, "{}?query={}".format(URL_REQUEST_TTF, title.replace(' ', '+').lower())]
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
    title = soupresult.find('h1', attrs={"itemprop":"name", "class": "game-title"})
    if title:
        title = title.find_next('a').text.strip()
    divdescript =  soupresult.find('div', attrs={'id': 'description'})
    description = divdescript.find_next('p').text
    casting = soupresult.find('div', attrs={'class': 'casting'})
    details = soupresult.find('div', attrs={'class': 'more_details'})
    shop = soupresult.find('div', attrs={'class': 'shops'})
    aref = casting.find_all('a')
    par = 0
    for a in aref:
        if 'Par' in a.previous:
            par = 1
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
    hdetail = details.find_next('h5', attrs={"class": "subtitle"})
    if hdetail.text == "Détails":
        pdetail = hdetail.find_next("p")
        date = int(pdetail.text.split(u'\xa0')[-1].strip())

    gameplay = soupresult.find('div', attrs={'class':'gameplay'})
    if gameplay:
        gameplay = gameplay.find_all('div', attrs={"class": "stat mini"})
        for play in gameplay:
            if play.find_next("div", attrs={"class": "sub"}).text == "Nombre de joueurs":
                players = play
                players.find_next('span').decompose()
                players.find_next('div', attrs={'class': 'sub'}).decompose()
                if players.text:
                   players = players.text.split('à')
                   playersmin = players[0].strip()
                   playersmax = players[1].strip()
                continue
            if play.find_next("div", attrs={"class": "sub"}).text == "Âge":
                agemintemp = play
                agemintemp.find_next('div', attrs={'class': 'sub'}).decompose()
                if agemintemp.text:
                    agemintemp = agemintemp.text
                    if "ans et +" in agemintemp:
                        agemin = agemintemp.strip('ans et +').strip()
                continue
            if play.find_next("div", attrs={"class": "sub"}).text == "Temps de partie":
                timemintemp = play
                timemintemp.find_next('span').decompose()
                timemintemp.find_next('div', attrs={'class': 'sub'}).decompose()
                if timemintemp.text:
                     timemin = timemintemp.text.strip()
                     timemax = timemin
                continue
    if shop:
        tarif = shop.find_next('div', attrs={'class': 'stat small'})
        if tarif:
            tarif.find_next('span').decompose()
            tarif = tarif.text.strip().split(u'\xa0')[0].replace(',','.')
    urls = [url, "{}?query={}&limit=20".format(URL_REQUEST_TRICTRAC, dbid)]
    newgame = {'title': title, 'description': description, 'date': date,
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
    #result = result.json()
    soupresult = BeautifulSoup(result.text)
    items = soupresult.find_all('a', attrs={"class": "w-full xl:w-1/2 px-3"}, href=True)
    #payload = {'query': query.replace(' ', '+').lower(), 'page': 2}
    #result2 = requests.get(URL_REQUEST_TTF, params=payload)
    #result2 = result2.json()
    #if result != result2:
    #    for r in result2['games']:
    #        result['games'].append(r)
    result = {}
    result['games'] = []
    for item in items:
        game = {'name': item['title'], 'id': item['href'].split('/')[-2], 'href': item['href']}
        print(game)
        result['games'].append(game)
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
        searchfield = self.request.GET.get('search_field',None)
        maxtime = self.request.GET.get('max_time', None)
        nbplay = self.request.GET.get('nb_play', None)
        if searchfield or maxtime or nbplay:
            context['view_search_field'] = ' '.join([searchfield, maxtime, nbplay])
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
