"""
Unit 7 Walk through 
User Authentication Login and Logout 

We'll learn how to create a user authentication system for logging in and out of the web app.
Users will be able to access certain pages when logged in that they cannot access when logged out.

We need a login page for new users. Django has a lot of this functionality built in by default.

# 
# 

1. Use Django's default login and logout views.

-> Open urls.py from the path below

[Rob]
mysite
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py             # mysite/urls.py
└── wsgi.py

#
#

2. Inside urls.py add the following import statement
"""
from django.contrib.auth import views as auth_views
"""

#
#

3. 
[Rob]

To set up login and logout routes in Django, you add URL patterns that point to Django’s
built-in authentication class-based views.

"""

path('login/',  auth_views.LoginView.as_view(), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
"""

The built-in views handle the authentication process for logging users in and securely terminating
their sessions.
As you'll see, all we have to do is create HTML template pages for login/logout, 
login being very similar to the register we have already created and logout being very small.

#
#

4. Run the development server and navigate to the login page to see the error.

-> python manage.py runserver
-> Go to http://127.0.0.1:8000/login/

[Rob]
-> Note the error: 

TemplateDoesNotExist at /login/

Exception Value:	registration/login.html

Django is looking for the template in a default location which does not exist. We can 
provide the path to the template we want to use via the 'template_name' parameter...

#
#

5. Update the urlpatterns list passing 
        template_name='users/login.html'
    
    (We are doing the same for logout).
"""
path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
"""
-> Refresh the development server 

[Rob]
-> Note the error: 

TemplateDoesNotExist at /login/

Exception Value:	users/login.html

->  Django is now looking for the template inside users now.
    Let's provide one.
#
#

6. Open: 
        users -> templates -> users ->
        
        & create:
        login.html and logout.html

[Rob]
 users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   ├── __init__.py
    ├── models.py
    ├── templates
    │   └── users
    │       └── login.html      #ADDED
    │       └── logout.html     #ADDED
    │       └── register.html
    ├── tests.py
    └── views.py

#
#

[Rob]
7. Start with login.html.
    Copy the code in register.html into login.html. 
    
Make the following changes...
a.  
    <legend class="border-bottom mb-4">Login</legend>                   # WAS: 'Join Here'
    
b. 
    <button class="btn btn-primary" type="submit">Login</button>        # WAS: 'Sign up'
    
c. 
        <small class="text-muted">
            Need An Account? <a class="ml-2" href="#">Sign Up Now</a>   # WAS: 'Sign In'
        </small>:
    

The login.html template should now look like this: 

{% extends "blog/base.html" %}
{% load crispy_forms_tags %}                    


{% block content %}
   <div class="content-section">
    <form method="POST">  
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Login</legend>
                {{ form|crispy }}               
        </fieldset>
        <div class="form-group">
            <button class="btn btn-primary" type="submit">Login</button>
        </div>
    </form>
    
    <div class="border-top pt-3">
        <small class="text-muted">
            Need An Account? <a class="ml-2" href="#">Sign Up Now</a>
        </small>
    </div>
   
   </div>
{% endblock content %}
"""

"""
7.1
Visit /login and observe the new login-page...

 #
 #

[Rob]
 7.2.
 Test the form by:
 a)
    Try to login with a user account that does not exist and

 b) 
    Try to login with a user account that does exist


a) For an account that does not exist:
    You will see that Django provides some functionality out of the box.
    An flash-message style error similar to the following should pop up.
 
    "Please enter a correct username and password. Note that both fields
        may be case-sensitive."
        
b) For an account that does exist:
    You will see something like...:
     
Page not found (404)
Request Method: 	GET
Request URL: 	    http://127.0.0.1:8000/accounts/profile/

By default Django attempts to navigate to /accounts/profile/.
We will add that later but for now we will redirect users
to the home page when they login.




12. When a user logs in redirect them to the home page.

--> Open settings.py from djang_project -> settings.py

django_project
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py

--> At the bottom of settings.py add the following
"""
LOGIN_REDIRECT_URL = 'blog-home'
"""
#
#

13. Retest the login page at http://127.0.0.1:8000/login with a correct user name and password. 
At this point you have a successful login and see the redirect back to the homepage. 


Session handling:
visit: /admin           (on /admin loading: logout if it shows a user is logged-in)

visit: /login (again)
-> Login with the user account that has admin privileges. (e.g. username: admin pasword: test)
-> Go to http://127.0.0.1:8000/admin
-> You will have access to the admin page
-> Logout

-> Login with the user account that does not have admin privileges  (username: test pasword: 1234test).
-> Go to http://127.0.0.1:8000/admin
-> A message like below is displayed...

        Site administration

        You don’t have permission to view or edit anything.


#
#


##
logout and re-visit
/register

open user/views.py -->register
& recall what happens if a valid form is submitted

register a new user:
Username: pinkpanther
email: pink@panther.com
password1: 1111test
password2: 1111test

& Submit*


14. Update the 
    /register 
    
    to redirect the newly created user to 
    'login' with their new credentials



Update to... 
"""
#See 'UPDATED' & 'CHANGE' below...
from .forms import UserRegisterForm                      
from django.contrib import messages              
               
def register(request):
    if request.method == "POST":                            
        form = UserRegisterForm(request.POST)               
        if form.is_valid():                     #UPDATED: msg below...
            messages.success(request, f'Account created for {username}, now you can login.')
            return redirect('login')            #CHANGED: was redirect('blog-home')
    #...

"""

15. Register another user and re-test. When a new successful
account has been added you will see a redirect to the login page.
e.g. 

Username: blackpanther
email: black@panther.com
password1: 1111test
password2: 1111test

& Submit*


--> python manage.py runserver
--> Go to: http://127.0.0.1:8000/register/
--> Redirect will bring you to http://127.0.0.1:8000/login/
        
and the success message will now display there

#
#

[Rob-]

[Rob]

16. Once logged-in a user will want to logout.


-> We will add to the 'blog/base.html' navbar... 
   
    NOTE: we are adding a <form> with a method="POST"
         and the {% csrf_token %} required by Django for post-requests.
          
    Recent  django.contrib.auth.LogoutView 
    only allows POST requests by default 
    (for security reasons — logging users out via GET can be abused with CSRF tricks). 
    So  if you visited /logout/ in the browser (which sends a GET), Django would reject
    it with "405 Method Not Allowed" error.
    
file: 'blog/base.html' see '# HERE' comments below for changes...    
...    
           <!-- Navbar Right Side -->

             <!-- # HERE: adjust bootstrap styling on the <div> 
                    ADD:
                    ... style="--bs-nav-link-padding-y: 0; -->           
            
            <div class="navbar-nav" style="--bs-nav-link-padding-y: 0;">
              <a class="nav-item nav-link" href="#">Login</a>
              <a class="nav-item nav-link" href="#">Register</a>

                <!-- # HERE: 
                        ADD: 'Logout' <form> with CSRF token  -->

                <form action="{% url 'logout' %}" method="post"  >
                    {% csrf_token %}
                    <button type="submit" class="nav-item nav-link ">Logout</button>
                </form>


            </div>
    


-> Above: clicking 'Logout' actually submits the <form>
    and the action on the form moves to the url for 'logout'.
    
    [Note: we previously defined /logout in mysite/urls.py
        to use the 'user/logout.html' template.]
    
    
    As such: we need to put some HTML in there...
    
    
    Open logout.html template...

└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   ├── __init__.py
    ├── models.py
    ├── templates
    │   └── users
    │       ├── login.html
    │       ├── logout.html             # HERE
    │       └── register.html
    ├── tests.py
    └── views.py

-> Place the following code inside logout.html


{% extends "blog/base.html" %}
{% block content %}
    <h2>You have been logged out</h2>
    <div class="border-top pt-3">
        <small class="text-muted">
             Login again <a href="{% url 'login' %}">Sign In</a>
        </small>
    </div>
{% endblock content %}

"""

"""


#
#

17. test the new logout template.

-> Run the development server
-> Open; http://127.0.0.1:8000/login/
-> Sign in with an account
-> Click the newly created 'Logout' option on the Navbar 
        that should now display....


We now have the functionality for Register, Login and Logout.

#
#



18. Next: update the 'blog/base.html' nav bar to 
    make the links for 'Login' and 'Register' 
    go to their respective routes...
    
    UPDATE the href="" of each to point to 
        {% url 'login' %}
        {% url 'register' %}
    
    e.g. like this...

 <div class="navbar-nav">
    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
    <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
 </div>


[Note: see mysite/urls.py to see name='login' and name='register']



 #
 #

19. Currently, we see always see 
        ... [Login][Logout][Register]
    
    on the nav-bar.

Typically, if you are
a) logged-in
    you shouldn't see 'Login' and 'Register' 
b) logged-out
    you shouldn't see 'Logout'
    
    
As such, we can use a conditional with the 
    
    is_authenticated 
    
property of

    django.contrib.auth.models.User.
    
See below:

<div class="navbar-nav" style="--bs-nav-link-padding-y: 0;">
    {% if user.is_authenticated %}
        <form action="{% url 'logout' %}" method="post">
            {% csrf_token %}
            <button type="submit" class="nav-item nav-link">Logout</button>
        </form>
    {% else %}
        <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
        <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
    {% endif %}
</div>



Test the new conditional by visiting
    /login
    
and ideally test each pathway of the conditional above.

[Rob-]

#
#

20. Add a restriction to certain routes. This is important in various situations. 
For the Blog application we
want to restrict users from editing their profile page until they have logged in. 
(i.e. you shouldn't be able to just visit /profile and see a Profile page.)
#
#

21.
Next let's create a Profile page and route:
Create  users -> templates -> users -> profile.html

users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    │   ├── __init__.py
    ├── models.py
    ├── templates
    │   └── users
    │       ├── login.html
    │       ├── logout.html
    │       ├── profile.html            # ADD
    │       └── register.html
    ├── tests.py
    └── views.py

-> After creating profile.html add the following code to display the username when logged in.

{% extends "blog/base.html" %}
{% load crispy_forms_tags %} 
{% block content %}
    <h1>{{ user.username }}</h1>    {# <!-- Just show a H1 username for now--> #}
{% endblock content %}

#
#

22. Define the route that will use this view.

Open urls.py from here ...

mysite/
  ├── __init__.py
  ├── asgi.py
  ├── settings.py
  ├── urls.py               # HERE
  └── wsgi.py

-> Update the urlpatterns list to include the profile route.
"""
   
path('profile/', user_views.profile, name='profile'),               # ADD
    

"""


Add a view function: to users/views.py...
"""

def profile(request):
    return render(request, 'users/profile.html')
"""


#
#

[Rob-]
23. Update the navbar to include a link to the profile page if the user is authenticated.
    See the comment with "ADDED profile link" below...


            <div class="navbar-nav" style="--bs-nav-link-padding-y: 0;">
                {% if user.is_authenticated %}
                
                    {# <!-- ADDED profile link  --> #}
                    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
                    
                    <form action="{% url 'logout' %}" method="post">
                        {% csrf_token %}
                        <button type="submit" class="nav-item nav-link">Logout</button>
                    </form>
                {% else %}
                    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                    <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>



#
#

24. Test the new view, template and route.

--> Run the development server; python manage.py runserver
--> Go to: http://127.0.0.1:8000/login and log in with an account
--> Go to: http://127.0.0.1:8000/profile you will see the user name displayed.
    for the user that logged in.

#
#

25. We need to put a check in place that ensures a user is logged in before they can go to 
http://127.0.0.1:8000/profile/

--> Open users/views.py from...
[Rob-]

To see the problem...
--> Run the development server; python manage.py runserver
--> Go to: http://127.0.0.1:8000/login and log in with an account
--> Go to; http://127.0.0.1:8000/profile at this point you will see the user name displayed.
--> Go to; http://127.0.0.1:8000/logout/
--> Press the back button on the browser or go to; http://127.0.0.1:8000/profile


 #
 #

 26. Django offers app decorators from django.contrib.auth.decorators. 
 We will import login_required and just above the profile view we will add the @login_required 
 decorator. 

"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Added import here
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully, now you can login.')
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required # Added decorator here
def profile(request): 
    return render(request, 'users/profile.html')
"""

#
#

27. Test the changes so far.


--> Run the development server; python manage.py runserver
--> Go to: http://127.0.0.1:8000/login and log in with an account
--> Go to; http://127.0.0.1:8000/profile at this point you will see the user name displayed.
--> Go to; http://127.0.0.1:8000/logout/
--> Press the back button on the browser or go to; http://127.0.0.1:8000/profile

At this point you will see an error as follows

Page not found (404)
Request Method: 	GET
Request URL: 	    http://127.0.0.1:8000/accounts/login/?next=/profile/


[NOTE: in the case the Profile page does display: 
        do a hard-refresh of the browser (it's likely displaying a cached version)
]

We can also add a @never_cache decorator to overcome this...


"""
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

#...

@login_required
@never_cache
def profile(request):
    return render(request, 'users/profile.html')
"""




#
#

28. Next: adding  a LOGIN_URL variable to mysite/settings.py 
    
    This tells Django where to redirect users when they try to access 
    a protected page without being logged in.
    So if a user hits a view with @login_required, they’ll be redirected to that URL.
    
    Specifically this will cause a redirect to /login in the case a logged-out user
    trys to visit /profile
    
--> Open mysite/settings.py from here 

mysite/
  ├── __init__.py
  ├── asgi.py
  ├── settings.py           # HERE
  ├── urls.py
  └── wsgi.py

--> Add this as the last line of the file

LOGIN_URL = 'login' 



[Rob-]
#
#
29.
[TASK: 
    comment-out the line and run the previous experiment
    using the browser's 'Back' button.
    Repeat the experiment with 
    
    LOGIN_URL = 'login'
    
    not commented (active)
...
e.g.

--> Run the development server; python manage.py runserver
--> Go to: http://127.0.0.1:8000/login and log in with an account
--> Go to; http://127.0.0.1:8000/profile at this point you will see the user name displayed.
--> Go to; http://127.0.0.1:8000/logout/
--> Press the back button on the browser or go to; http://127.0.0.1:8000/profile

At this point you will be redirected back to http://127.0.0.1:8000/login/?next=/profile/



##
In Django, the @login_required decorator (or LoginRequiredMixin) is what causes:

/login/?next=/profile/


@login_required blocks access to /profile/ if you’re not logged in

Django then redirects you to LOGIN_URL (/login/)

It adds ?next=/profile/ so it can send you back after you then login.




##

At this point we have implemented a basic authorization system with Django.


30.
[Rob]
##
As a final finshing touch: 


    Both register.html and login.html have 
    links with href="#".
    
    Let's update the links:
        login    --> link to register (if you don't have an account)
        register --> link to login    (if you already have an account)


Ensure they are updated to direct the user the the appropriate pages...

register.html:
        Already Have An Account? <a class="ml-2" href="{% url 'login' %}">Sign In</a>

login.html
        Need An Account?         <a class="ml-2" href="{% url 'register' %}">Sign Up Now</a>

"""









