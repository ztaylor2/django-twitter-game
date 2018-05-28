# django-twitter-game
An app similar to twitter that has a game with each post.

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
