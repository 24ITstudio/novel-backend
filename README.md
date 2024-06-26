
# novel library backend
[![novel library](https://github.com/24ITstudio/novel-backend/actions/workflows/python-app.yml/badge.svg)](https://github.com/24ITstudio/novel-backend/actions/workflows/python-app.yml)


## What's this
A backend that provides API for self-hosting novel reading.

- self-hosting: novels are stored in server's database.
- user-system: support registration, login and so on.

## Doc
see [novel-doc](https://github.com/24ITstudio/novel-doc)


## Get started
After this repo is cloned,
firstly `cd novel_backend` to go to the django project, then run `python manage.py migrate` to generate a new datebase (`db.sqlite` has been added to `.gitignore`).

Next, just `python manage.py runserver` as you like!


## Project tree

`/novel_backend` is the django project, which contains `manage.py`

`/novel_backend/novel` defines the novel model


`/novel_backend/novel_backend` is the main server app

`/requirements.txt` contains the dependencies, used when `pip install -r requirements.txt`

