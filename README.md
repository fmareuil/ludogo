# ludogo

A django application to make a personal movie and board game library.

To customize your home page, add images in :
* common/static/common/images/add_game.png
* common/static/common/images/add_movie.png 
* common/static/common/images/search_game.png
* common/static/common/images/search_movie.png 

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
* with the invit commands windows:
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
