# django-twitter-game

## About

Built on Python's Django framework. Background tasks such as determining
the validity of a post an hour after creation are handled with the
django-background-tasks package. 

There are two sub folders for the twitter_game app:
twitter_game, and posts. twitter_game handles the
homepage view. posts handles everything that has to do with a post such
as the post, like, and dislike models, the post create view, and the
like and dislike routes. 

The code that handles the background tasks can be found in posts/models.py. 

## Getting Started 

- Ensure Python 3 is installed 
- Start Python 3 virtual environment in root directory (django-twitter-game)
    - `python3 -m venv ENV`
- Install dependencies 
    - `pip install -r requirements.txt`
- Create PostgreSQL database 
    - `createdb twittergame`
- Setup Database 
    - `cd twitter_game`
    - `./manage.py makemigrations`
    - `./manage.py migrate`
- Run app locally 
    - `./manage.py runserver`
- Setup another tab to run background tasks
    - Open up a new tab in terminal
    - Activate the environment in that tab
    - Run `./manage.py process_tasks`
- View app in web browser 
    - `http://localhost:8000/`
