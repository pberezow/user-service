#Documentation

Service requires:
- Python 3.6
- gunicorn3
- database engine (PostgreSQL)
- python's packages listed in `requirements.txt` file (There is recomended to use python's virtual environment)

Service runs on port 3000. 

This microservice handles all functionalities related to user actions, including:
- registration of new users
- login (using JSON Web Token)
- logout
- getting informations about users
- deleting users
- editing users (password + other data)
- creating permission groups
- editing permission groups
- assigning permission groups to user

##Project Structure

All implementation is located in server module. In server `__init__.py` there is all flask application 
and Eureka related code. 

All server configuration is located in `config.py` and `gunicorn.conf.py` file. 

In `keys` directory there are files with SSH keys used to encode and decode JWT. 

In `routes` module there are all api endpoints defined.

In `models` module there is everything related to database, like tables and transport objects. 
It also contains classes used to validate request payloads.

There are also 2 modules, `users` and `groups`, which contains logic implementation to defined endpoints.


##Running service
First you should install everything required by app to run.

When you want to run microservice, first you should run Eureka, then run command:

- dev mode (without gunicorn):
```
python manage.py run
```

- regular startup:
```
python manage.py start
```

There is also `Dockerfile` provided, if you want to use docker. 
To build image run:
```
docker build -t user_service:latest .
```

and then run image with:
```
docker run -d -p 3000:3000 user_service
```