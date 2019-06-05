@echo off
cmd /k "%UserProfile%\Envs\venvludogo\Scripts\activate & cd /D %~dp0..\  & python manage.py runserver" 

