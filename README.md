# ludogo <img src="/common/static/common/images/ludogo_icon.png" width="100"/>

A django application to make a personal movie and board game library.

To customize your home page, add images in :
* common/static/common/images/add_game.png
* common/static/common/images/add_movie.png 
* common/static/common/images/search_game.png
* common/static/common/images/search_movie.png 

In most of the cases for each entry, game or movie, all informations can be recovered from the internet accessible databases with the search button.
But in some case you have to add information manually. Use the admin interface to add localisation, game genres, langues movie, format movie (mandatory) and if necessary, to add person, all other information can be add by the classical ludogo web interface from an empty page (movie or game).

## To deploy on linux:

* git clone https://github.com/fmareuil/ludogo.git
* python3 -m venv venvludogo
* source venvludogo/bin/activate
* cd ludogo
* pip install -r requirement.txt
* python manage.py createsuperuser
* python manage.py runserver

## To deploy on windows:
* install git for windows https://git-scm.com/download/win
* install python3 from https://python.org/downloads/ Check the box next to Add Python 3.5 to PATH and then click Install Now.
* use git to clone source: 
  - launch git bash application 
  - git clone https://github.com/fmareuil/ludogo.git
* with the Windows command prompt:
  - pip install virtualenvwrapper-win
  - mkvirtualenv venvludogo
  - workon venvludogo
  - cd pathtoludogo
  - pip install -r requirement.txt
  - python manage.py createsuperuser
  - python manage.py runserver

# Remarks

* You can deploy it at a particular ip to access it from your local network, by default django webserver are accessible at the url http://127.0.0.1:8000
* We don't recommand to give access to your ludogo to internet. There is no authentification system.
