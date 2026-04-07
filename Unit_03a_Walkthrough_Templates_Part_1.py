"""
Unit 3 Walk through Part 1
Django Templates 
Now we will use return render instead of HTTPResponse

# 
# 

1. Create a templates directory inside the blog app

Before ... 
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


After ...
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
    ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py

# 
# 

2. Django looks for a templates sub directory in all installed apps. To ensure we are pointing to the correct
templates we need to create another directory called blog and inside of this we have our .html templates.

blog -> templates -> blog -> .html files.

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── blog
│   │       ├── about.html
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py

# 
# 

3. Inside the html files create some boiler plate HTML. Inside VS code use ! then press enter 
for boiler plate html. Add a h1 to each page with similar content.

#
# [Rob]
# Note the '!' inside the <h1> (previously no '!')


<body>
    <h1>Blog Home!</h1>
</body>

<body>
    <h1>Blog About!</h1>
</body>


# 
# [ROB]
# At this point: 
#  a) save all files
#  b) try visit /blog/
#
#  is it using the new home.html?...
# 

4. For Django to correctly use your templates we need to add the app configuration to the 
settings.py module. To find our app configuration open apps.py from the blog directory.

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py 
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── blog
│   │       ├── about.html
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py

# 
# 

5. apps.py
Inside the file we see class BlogConfig(AppConfig): BlogConfig inherits from AppConfig.
Copy the class name BlogConfig.
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

"""

# 
# 

6. Open settings.py from django_project and use the BlogConfig class name to add the list of INSTALLED APPS.

├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

Inside settings.py we are looking for INSTALLED APPS.
"""
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

"""

Add the following string "blog.apps.BlogConfig",

"""
INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

"""
Anytime you create a new app you need to add it to this list.

# 
# 

7. We now need to to get Django to render the template when a user navigates to
a page. We need to point our blog views.py to use the templates. 
Open up views.py from Blog.

├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py 
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── blog
│   │       ├── about.html
│   │       └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py

Inside views.py we will now use the default Django import
to render the template.  
from django.shortcuts import render

Update the functions views.py from this...
"""
def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

def about(request):
    return HttpResponse('<h1>Blog About</h1>')

"""
to this
"""

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return HttpResponse('<h1>Blog About</h1>')

"""

# 
# 

8. Run the development server from the command line python manage.py runserver
Test the pages and view the source code on the browser.
At this point if you where to only use static pages with Django you would simply
add more routes / templates and css but most sites are dynamic

# [Rob]
# 8.1 Updating views to render() .html templates 
#       instead of returning  HTTPResponse()
#     [Note: after updating home() do about(): then visit and test both.]
#     [Note: we're not using Django templating yet, just setting up for it.]

"""  
# views.py: updated home() & about() 
def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

"""



# 
# 

9. Add a list to views.py that contains a dictionary with key value pairs.

"""
from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        "author": "Bill Tutman",
        "title": "Getting Started with Django",
        "content": "A django basics and understandings post.",
        "date_posted": "05/02/2026"
    },

    {
        "author": "Djan Gu",
        "title": "Don't forget the django tutorial",
        "content": "Exploring frameworks like django post.",
        "date_posted": "18/03/2026"
    }
]
"""



Imagine we have made a database call to return the posts and would like to 
display them on the home page.

#
#



10. Inside the home() create a dictionary that will pass the posts via return render.
"""
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

"""

The context dictionary is passed to render(). Inside the context dictionary
the key: value pair 'post': posts is using the posts list above.

#
#

11. Open home.html from blog -> templates -> blog - home.html
We will edit the template to display the blog posts.

--Using a for loop

Inside the <body> remove the original h1 and add the following

<body>
    {% for post in posts %}
        <h1>{{ post.title }}</h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content}}</p>
    {% endfor %}
</body>

Save the file and test the page. View page source to show the HTML elements 
that have been created by the template engine that Django uses.

This is very similar to Jinja 2 we have seen from Flask.

#
#

12. Update the home.html and about.html templates to the following code. We will pass a title

-- Using If / else

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width= , initial-scale=1.0">
    {% if title %}
        <title> Django Blog - {{ title }}</title>
    {% else %}
        <title>Django Blog</title>
    {% endif %}
    
</head>




13.Update views.py to add a title for the about function to the following code.
"""
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

"""
# [Rob]
Run the server and test both home() and about() views. 
Notice the home() doesn't pass a title yet so the else block from part 12
home.html template is triggered. 
The about() does pass a title so the if block runs: see the browser's tab
    for the title passed.


#
#
# [ROB]
# 13.1 Update the home() functions 'context' dict:
    context_dict={
        'posts': posts,
        'title': 'rob-title'
    }
    
    TASK: 
    Can you alter the template code to access the context_dict's title value?

# Ensure all changed files are saved
# Reload the browser /blog/ route
# See the browswer tab's title text matches what we set in the context_dict



#
#

Currently our templates are not a very good design. Both the
home.html and about.html templates have very similar code.
The issue is as the code base grows changes become challenging
with redundant code. A better solution is to use template inheritance.


# 
# 

14. Create a base.html file inside blog -> templates -> blog

blog
│  ├── __init__.py
│  ├── __pycache__
│  ├── admin.py
│  ├── apps.py
│  ├── migrations
       ├── __init__.py
│  ├── models.py
│  ├── templates
│  │   └── blog
│  │       ├── about.html
│  │       ├── base.html
│  │       └── home.html
│  ├── tests.py
│  ├── urls.py
│  └── views.py

# 
# 

15. The html in both html files is very similar. 

# [Rob]
Create base.html with boiler-plate html
# (e.g. VSCode shorcut: !+Enter )

Move (cut-paste) the head section from home.html into base so you have:
file: base.html:

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width= , initial-scale=1.0">
        {% if title %}
            <title> Django Blog - {{ title }}</title>
        {% else %}
            <title>Django Blog</title>
        {% endif %}
        
    </head>

    <body>
        
    </body>

</html>


This code will be the shared code of both .html files.
Add in template block markers inside the <body>:


<body>

    {% block content %}{% endblock %}
    
</body>



This {% block content %}{% endblock %} can be overidden in 
the extending files.



# 
#
16. Update home.html: add the following as the first line.

{% extends "blog/base.html" %}
    
Remove <body> tags if still present and then add the 
content-block markers around the previous template code
so you then have: 

"""
{% extends "blog/base.html" %}

{% block content %}

    {% for post in posts %}
        <h1>{{ post.title }}</h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}

{% endblock %}
"""


# 
#
17. Save all changed files and visit the /blog route.
    View page source.



18. Update about.html to the following code. <h1>Blog About!</h1>
is the only unique item on this page. Placing this inside block
{% block content %} {% endblock content %} overides the base.html
implementation.

    {% extends "blog/base.html" %}
    {% block content %}
        <h1>Blog About!</h1>
    {% endblock content %}





    
# 
#

19. To see why template inheritance is so powerful we will show some examples using
Bootstrap. We will use some information from the starter template in our base.html file 
https://getbootstrap.com/docs/5.3/getting-started/introduction/


# 
#

20. Update the base.html file to include the cdn and option 1 script.

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">

        
        {% if title %}
            <title> Django Blog - {{ title }}</title>
        {% else %}
            <title>Django Blog</title>
        {% endif %} 
    </head>
    <body>
        {% block content %}{% endblock %}
    
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>

    </body>
    </html> 

#
#

21. Update the base.html: add a <div> wrapper with Bootstrap class = container.
    This will to add some margin and padding to the app.

    <body>
        <div class = "container">
            {% block content %}{% endblock %}
        </div>



At this point test the app and you will some changes to the margin and padding on both the
home and about pages. The css takes effect on both pages due to template inheritance.
"""


