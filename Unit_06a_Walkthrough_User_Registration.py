"""
Unit 6a Walk through 
User Registration 

[Rob]
General Users should not have direct access to the admin page.
Typically, the admin page is used by administrators, staff, and 
developers for 
    managing content, 
    user accounts, 
    system settings, and
    overseeing overall application operations.

As such, there's a need to provide our own register/login/logout and
edit-post type front-ends (for general users). 

The typical approach for this is to start a new Django app
which creates a new sub-folder...

djangoproject/
    |-  mysite/
    |-  blog/
    |-  users/                                  #Added!
    
/blog and /users will have the same structure...

The logic is that we can provide
User-specific:
    * URLConf's (or "end-points" or "routes")
        e.g. 
            - mysite/urls.py
            - users/urls.py
                urlpatterns=[
                    path(...),
                ]
    
    * .html template files 
            users/templates/users/
                              |- login.html
                              |- logout.html
                              |- register.html
                              ...
                                 etc. 
    * views.py logic
            users/views.py
                    |- def register(request)
                    |- def login(request)
                    |- def logout(request)
                    |- ...
                            etc.
        (we can extend Django's django.contrib.auth.forms here and specialize) 
    
    * models.py classes to represent DB User entities
        (we can extend Django's django.db.models.Model here and specialize)                    
    

# 
# 

[Rob]
1. Create a new app for Users. 
    In a terminal, from djangoproject/ 

python manage.py startapp users


This will create the users app and your project tree structure should reflect something similar to
the following.

django_project
    ├── blog
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── static
    │   │   └── blog
    │   │       └── main.css
    │   ├── templates
    │   │   └── blog
    │   │      ├── about.html
    │   │       ├── base.html
    │   │       └── home.html
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
    ├── manage.py
    └── users
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        │   └── __init__.py
        ├── models.py
        ├── tests.py
        └── views.py


#
#

2. At this point we want to add a user registration page on the front-end for users to
register. The first thing we need to do is add our new created app to the INSTALLED APPS LIST
in settings.py.

file: django_project/mysite/settings.py
Open settings.py and the list should contain the following

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

#
#

[Rob]

4. Update the INSTALLED_APPS list with "users.apps.UsersConfig"
"""

INSTALLED_APPS = [
    "users.apps.UsersConfig",
    "blog.apps.BlogConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
"""




# [Note: The above "users.apps.UsersConfig" refers to
    djangoproject/users/app.py
    
    You will see it contains a class that looks something like this...

class UsersConfig(AppConfig):
    name = 'users'

#
#

#
#

5. Open views.py 
    file: djangoproject/users/views.py 
    
    We want to create a form for Users to 'Create Account' or 'Register'.
    Similar to the database models (django.db.models.Model), django has some
    pre-defined classes we can use for this....
    Import the UserCreationForm module as follows.
"""
from django.contrib.auth.forms import UserCreationForm
"""

#
#

6. Create a register view in views.py and to use the form
"""
def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
"""

-> form = UserCreationForm()                            

#
# Creates a new form object.

-> return render(request, 'users/register.html', {'form': form}) 

#
# We pass that form Object to the render() function for use when 
     rendering the register.html template.

#
#
djangoproject/users/views.py should now have the following code:

"""
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

"""

#
#

7. Create the template for the register view. We have done this before.
As a reminder the Django convention is to create the following strucuture

users -> templates -> users -> register.html (All templates for the users app go here)

The users tree structure should now be as follows.

users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── templates
    │   └── users
    │       └── register.html
    ├── tests.py
    └── views.py

#
#

8. As before we want to extend the template. We already have base template so we can use the following
code in register.html. We can reference base.html even though is inside another app.

file: user/register.html

{% extends "blog/base.html" %}
{% block content %}
  
{% endblock %}

#
#

9. 
Create a <div> inside the block as follows (and add a Bootstrap class).

    {% extends "blog/base.html" %}
    {% block content %}
       <div class="content-section">
        
       </div>
    {% endblock content %}

#
#

10. Within the <div> create a <form> with the method POST.

    {% extends "blog/base.html" %}
    {% block content %}
        <div class=""content-section>
            <form method="POST">  
                
            </form>
        </div>
    {% endblock content %}

#
#

11. Add a CSRF (Cross-Site Request Forgery) token. 

    {% extends "blog/base.html" %}
    {% block content %}
        <div class=""content-section>
            <form method="POST">  
                {% csrf_token %}                            #ADDED
            </form>
        </div>
    {% endblock content %}
    
In Django, any HTML form that sends data using the POST method must 
include a CSRF (Cross-Site Request Forgery) token. 
    [WARNING: A Django POST form will not work without a CSRF token.]
    
This token is a built-in security feature that helps protect your 
application from malicious requests made by other sites.




#
#
[Rob]
12. Below we can add a <fieldset class="form-group"> 
    with a 'Join Here' as a 
        <legend class="border-bottom mb-4"> 
    for styling.

    {% extends "blog/base.html" %}
    {% block content %}
        <div class=""content-section>
            <form method="POST">  
                {% csrf_token %}
                <fieldset class="form-group">
                    <legend class="border-bottom mb-4">Join Here</legend>
                </fieldset>
            </form>
        </div>
    {% endblock content %}

#
#

[Rob]
13. With the {% csrf_token %} in place, the form can be rendered 
    where the context {'form': form} Object passed to the template
    (in views.py) can be referred to using the variable 'form'.

    Below: we refer to this 'form' adding django's: '.as_p' method
    
    [Note: Django doesn't require the '()' for functions, it does this for us.]
    
        {{ form.as_p }} 
        
    The as_p, will take each filed from the form Object and display each 
    in seperate <p> tags to give basic formatting.

    {% extends "blog/base.html" %}
    {% block content %}
        <div class=""content-section>
            <form method="POST">  
                {% csrf_token %}
                <fieldset class="form-group">
                    <legend class="border-bottom mb-4">Join Here</legend>
                {{ form.as_p }}
                </fieldset>
            </form>
        </div>
    {% endblock content %}

#
#

14. Below we add a submit button with some typical Bootstrap styling classes.

    {% extends "blog/base.html" %}
    {% block content %}
        <div class=""content-section>
            <form method="POST">  
                {% csrf_token %}
                <fieldset class="form-group">
                    <legend class="border-bottom mb-4">Join Here</legend>
                    {{ form.as_p }}
                </fieldset>

                    <div class="form-group">
                    <button class="btn btn-primary" type="submit">Sign Up</button>
                    </div>

            </form>
        </div>
    {% endblock content %}

#
#

15. Next we can add a section on the form for signing in if a user already has an account.
    Also adding some BootStrap classes for styling.

    {% extends "blog/base.html" %}
    {% block content %}
        <div class="content-section">
            <form method="POST">  
                {% csrf_token %}
                <fieldset class="form-group">
                    <legend class="border-bottom mb-4">Join Here</legend>
                    {{ form.as_p }}
                </fieldset>
                <div class="form-group">
                    <button class="btn btn-primary" type="submit">Sign Up</button>
                </div>
            </form>

            <div class="border-top pt-3">
                <small class="text-muted">
                    Already hava an account? <a class="ml-2" href="#">Sign In</a>
                </small>
            </div>

        </div>
    {% endblock content %}
    

#
#

16. At this point we need to create a url pattern to use this view when the page is requested.
Open: mysite urls.py (django_project/mysite/urls.py).

mysite/
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py

Update urls.py to the following
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('blog/',include('blog.urls')),
    path('register/', user_views.register, name='register'),
]

"""
[Rob]
Note: above we could have just added:
"""
from users import views
urlpatterns = [
    path('register/' views.register, name='register'),
    #...
]
"""

but we're choosing to show that:

a) we can **directly** refer to an app's views in mysite.urls (urls.py)
        without using and include() to users/urls.py
        
b) in such case, the use of a Python alias ('as')
    serves to distinguish users/views from any other
    app views that may be included: e.g. if we also had
    
        from blog import views 
    
    we could distinguish _it_ with:
    
        from blog import views as blog_views 


    so then 'blog_views' would refer to blog/views
    and     'user_views' would refer to user/views
#
#



17. At this point: view the app in the browser. 

-> python manage.py runserver
-> Go to http://127.0.0.1:8000/register

You will now see the form and all of the default details Django gives us out of the box.

[Rob]
17.1 View page source and examine the <p> elements: 
        where do you think they come from?
#
#






18. At this points if we try to use the form nothing will happen bar a redirect. 
In our register view any request that comes in we are creating a blank form and 
rendering it out to the template. With HTTP requests we have different options.
Commonly used are POST and GET.

If we get a POST request we can put a check in place to validate the form information
and if we have a GET request leave the redirect.

Update views.py 
[Rob]
file: users/views.py

users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── templates
    │   └── users
    │       └── register.html
    ├── tests.py
    └── views.py

"""

"""
Try beginner step:
"""
##1. Begin:
def register(request):
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form':form} )

#& visit /register

##2. Move to...
def register(request):
    if request.method == "POST":                            #if POST request
        form = UserCreationForm(request.POST)               # populate Form obj' with POST data
        username = form.data.get('username')                # get the 'username' from the Form obj'

        #[Rob]
        #just show we can send extracted username from the form data
        return render(request, 'users/register.html', {'form': form, 'user': username})
    else:
        #[Rob]
        # send empty form object to be rendered with Django's form.as_p()
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form':form} )

