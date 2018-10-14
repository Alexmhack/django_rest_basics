# Django-Rest-Basics
Basic Django Rest API project for learning purposes

Create ```virtualenv``` using

```
# automatically gets activated
mkvirtualenv rest
```

Install packages separately using
```
pip install django djangorestframework djangorestframework-jwt python-decouple
```

Or from ```requirements.txt``` file in the repo

```
pip install -r requirements.txt
```

Start Django project and app

```
django-admin startproject cfehome .
python manage.py startapp postings
```

Add ```postings``` in ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django apps
    'postings',
]
```

And use **environment** variables for django **SECRET_KEY**

Create ```.env``` file in root folder and fill it with ```SECRET_KEY``` from ```cfehome/settings.py```

**.env**
```
PROJECT_KEY=your_secret_key
```

```
from decouple import config
...

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('PROJECT_KEY')
```

Run migrations, create super user and run server

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configure REST FRAMEWORK
Update project **settings** to reflect the following changes

```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'postings'
]



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```
