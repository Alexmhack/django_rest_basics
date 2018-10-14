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

## Implementation
For **postings** folder we create a sub python module named **api** which will contain 
all the files for **postings** app *API*

Just like django **Model-View-Controller** ```rest_framework``` also works on the same
principle.

We have three files:

1. ```api/serializers.py```
2. ```api/views.py```
3. ```api/urls.py```

**Serializers** convert the data into json objects and also validates over that data.
Rest Framework **Generic Views** work just like generic views from Django -> **Create 
Retrieve Update Delete** Views.

But before working with views we need to create a serializer, which can be done using the 
model serializer which means the serializer is based on the app model

```
from rest_framework import serializers

from postings.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('pk', 'user', 'title', 'content', 'timestamp')
        read_only_fields = ('user',)
```

And along with that we can create a validate method for the model serializer which has 
syntax ```validate_<field_name>``` or alltogether ```validate``` which validates over all 
fields

```
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('pk', 'user', 'title', 'content', 'timestamp')
        read_only_fields = ('user',)

        # serializer converts to json and validates the data
        
    # validate_<field_name>
    def validate_title(self, value):
        qs = Blog.objects.filter(title__iexact=value)

        # excludes the instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value
```

Now we can use this model serializer in our views.

```generics.RetrieveUpdateDestroyAPIView``` gives the three main methods for the model instances namely **GET PUT DELETE** which does not include ```Create``` view or the **POST** method.

```
class BlogRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all().order_by('-timestamp')
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #   return Blog.objects.all()
```

You can either define the ```get_queryset``` method or use ```queryset``` option, refer
[docs](https://www.django-rest-framework.org/api-guide/generic-views/#methods) for more info.

With our views and models defined we just need the url endpoints for the API. Here comes the use of ```api/urls.py``` file. Which are simple url paths made from ```django.urls.path```

```
from django.urls import path

from .views import BlogRUDView

app_name = 'api-postings'

urlpatterns = [
    path('<int:pk>', BlogRUDView.as_view(), name='blog-rud'),
]
```

But before continuing we need to include these api urls in project urls

**cfehome/urls.py**
```
...
# api endpoints
urlpatterns += [
    path('api/blog/', include('postings.api.urls', namespace='api-postings')),
]
```

Now run the server and on the [admin](http://127.0.0.1:8000/admin) site create some blog 
posts that and then go to [127.0.0.1:8000/api/blog/1](http://127.0.0.1:8000/api/blog/1)

You will find all the fields that we defined in the ```ModelSerializer``` in json data 
format. If you cannot access the url and get an error saying

```
HTTP 401 Unauthorized
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
WWW-Authenticate: JWT realm="api"

{
    "detail": "Authentication credentials were not provided."
}
```

This comes from the ```permission_classes = (IsAuthenticated,)``` in ```BlogRUDView```
which makes this view accessible to only the authenticated users, there is also ```IsAdminUser``` which gives permission to users with ```is staff``` flag **True**.

## REST [Mixin](https://www.django-rest-framework.org/api-guide/generic-views/#mixins)
Django REST Framework has a seperate view for Create Operation called the [CreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#createapiview) that works very similarly to [CreateView](https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#createview) in django.

But we will be implementing a post method using [mixins](https://www.django-rest-framework.org/api-guide/generic-views/#createmodelmixin) which gives ```.create``` method which is then used in post request,

```
class BlogListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.all().order_by('-timestamp')

    # add create as well as list functionality to view
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # adds the post method in allowed methods list
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

And the url for this view will be like

```
urlpatterns = [
    path('', BlogListAPIView.as_view(), name='blog-list'),
    ...
```

Now on visting [127.0.0.1:8000/api/blog/](http://127.0.0.1:8000/api/blog/) you get **POST** method as well as **GET** method, the get method gives the list of blogs and on 
filling the form in the bottom of page you can create a blog.
