"""
Unit 2 Walk through
Django Create and app and url routes 

# 
# 

1. Create a blog app inside the website project. This can be confusing but Django
uses a website project and inside this you can have multiple apps. For example
your website could have a blog and and a store app. We can separate out large projects
into separate apps You can also take an app you have created and use it in other projects.

python manage.py startapp blog

# 
# 

2. Show tree structure. tree in Terminal or VS Code etc

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

The blog directory has been created from python manage.py startapp blog.
There is a lot of files here but we will step through them.

# 
# 

3.Open blog/views.py

You will see from django.shortcuts import render

# Create your views here.

# 
# 

4. import HttpResponse

from django.http import HttpResponse

#
#

5. Create our first function. The logic for where we want the user to go

"""

def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

#
#

"""
6. Create a file in the blog app named urls.py

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py


#
#

7. Inside urls.py in the blog directory we will add something similar
to the urls.py file inside the django_project directory
"""

from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

#
#

"""
8. We need to use the function home() created in part 5 above.
We need to import the file from the current directory.
urls.py is now updated to 
"""

from django.urls import path
from .import views

urlpatterns = [
    path("admin/", admin.site.urls),
]

#
#

"""
9. In the path of url patterns we need to specify the view we want to handle 
the logic for the home page.
"""

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='blog-home'),
]

"""
views.home is accessing the home functions from views.py.
name='blog-name' is giving a unique name to the page.
It's important to be specific here and not just name it home as this
may cause a clash with other apps. For example another app could also
be name 'home'

#
#

10. We need to add one more thing to get this up and running.
Inside the main django_project website we need to specify the
the url for the blog app. To be clear the url.py file we are 
changing is in this directory.

├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

11. We are adding two things to the urls.py file. Firstly, the 
include function and the specific path.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/",include('blog.urls')),
]

"""
When we run the project and go to the blog app the blog urls
are included. Inside the blog urls.py the path the maps onto 
views.home as below.
"""

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='blog-home'),
]

#
#

"""
12. Make sure you are in the django_project directory where manage.py is on the command line
and run the the project to test with python manage.py runserver

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

"""
#
#

"""
13. When you navigate to the development server at http://127.0.0.1:8000/ 
At this point what you get is a 404 error. The command line will show something
similar to this

Not Found: /
[11/Jul/2023 16:07:03] "GET / HTTP/1.1" 404 2172


On the webpage you see something similar to below.

Page not found (404)
Request Method: GET
Request URL:    http://127.0.0.1:8000/

Using the URLconf defined in django_project.urls, Django tried these URL patterns, in this order:

admin/
blog/
The empty path didn’t match any of these.

You are seeing this error because you have DEBUG = True in your Django settings file. 
Change that to False, and Django will display a standard 404 page.


#
#

14. Note that Django tried the url patterns in this order 

Using the URLconf defined in django_project.urls, Django tried these URL patterns, in this order:

admin/
blog/

The empty path did not match any of these.

#
#

15. Navigate to http://127.0.0.1:8000/blog
The page now loads. View page source to see
<h1>Blog Home</h1> 

#
#

16. Now we will add another page and route.
- Step 1 is to edit views.py
- Step 2 is to edit urls.py in the blog app for mapping
- Step 3 Run and test

17. Step 1 add the following function to views.py
"""

def about(request):
    return HttpResponse('<h1>Blog-About</h1>')

"""
#
#

18. Step 2 update urls.py in blog to the following
"""
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='blog-name'),
    path('about/',views.about, name='blog-about'),
]

#
#

"""
19. Step 3 run server if stopped and navigate to 
http://127.0.0.1:8000/blog/about/

You will now see the page with 
<h1>Blog About</h1>

At this point you have Blog Home and Blog About pages

#
#

20.Whats happening here in order when going to http://127.0.0.1:8000/blog/about/
is as follows.

a) urls.py in django_project looks for the blog app to see is there a matching pattern
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/",include('blog.urls')),
] 

"""
There is one here... path("blog/",include('blog.urls')),

b) Once the path is found it then goes to blog.urls. In blog.urls it
then looks for an about route. 
"""
urlpatterns = [
    path('', views.home, name='blog-name'),
    path('about/',views.about, name='blog-about'),
]

"""
There is one here... path('about/',views.about, name='blog-about'),

c) At this point we navigate to the views.about function.


#
#

21. This might seem complex to have the url jump around like this but
it can actually be very useful if we don't want a live environment but a testing
environment.

For example I can update urls.py from here

├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py

Before...
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/",include('blog.urls')),
]

"""
After...
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog_dev/",include('blog.urls')),
]

"""
Now my app loads at
http://127.0.0.1:8000/blog_dev
http://127.0.0.1:8000/blog_dev/about

#
#

22.To set the blog home page to open without navigating to http://127.0.0.1:8000/blog
we update urls.py from here

├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py


to...

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('blog.urls')),
]





