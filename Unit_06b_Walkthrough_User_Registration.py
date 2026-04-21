"""
Unit 6b Walk through 
User Registration - POST data



[Rob]
18. Capture a POST request and data

    Visit 
        /register
    Enter something like...
        Username:   test, 
        Password:   test, 
        Password:   test 
    
    & 'Sign-Up' (/Submit)
    
    
    Notice that the page refreshes and
    remains on the /register route.
        
    Observe the server log:
        "POST /register/ HTTP/1.1" 200 4732
    
    [Repeating the operation confirms this via the repeated server log record]
        "POST /register/ HTTP/1.1" 200 4732
        "POST /register/ HTTP/1.1" 200 4732


Update views.py 
file: users/views.py

"""
def register(request):
    if request.method == "POST":                            #if POST request
        form = UserCreationForm(request.POST)               # populate a Form obj' with data from the 'Submit'
        username = form.data.get('username')                # get the 'username' from that Form obj'

        #[Rob]
        # Below: 
        # Sending the form as 'form' and the extracted 'username' above, as 'user'
        #  [These terms can be referred to in the template to access that data]
        return render(request, 'users/register.html', {'form': form, 'user': username})
    else:
        #[Rob]
        # else (not a POST request)
        # Send empty form object to be rendered with Django's form.as_p()
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form':form} )


"""
18.1
    Add the following to the top of users/register.html:
    file: users/templates/users/register.html
    
        {% if user %}
            <p style="color:red;">Retrieved from render() - 'user': {{user}}</p>
        {% endif %}
        
    Save & re-visit the /register route.
    
    Notice: 
    
        - Retrieved from render() - 'user': AnonymousUser
    
        displays at the top of the page.
        [Note: if logged-in (from /admin say) you may see that logged-in username
               instead of 'AnonymousUser'
        ]
    
18.2 - Fill the form and click Submit: 
    
    Enter something like
        testy, testy, testy 

    Notice the message above is _now_ rendered at the top of the page (with something like): 
    
    -   Retrieved from render() - 'user': testy
    
    - TASK: explain how that happened.
     
    [Notice: 
        - the 'else' runs when just visit /register
        - the 'if'   runs when adding data and clicking Submit 
    ]
    
 
 18.3 - Repeat but this time access the form data in the template:
 
    Add this to register.html:
    
        {% if form %}
            <ul style="color:orange;">
                <p>Retrieved from render() - 'form' ...</p>
                <li>form.username:  {{form.data.username}}</li>
                <li>form.password1: {{form.data.password1}}</li>
                <li>form.password2: {{form.data.password2}}</li>
            </ul>
        {% endif %}
        
    [Notice: 
        If you inspect the page and expand the <p> elements 
        generated from 
        
            {{ form.as_p }}
            
        you can see how the attribute names 'username', 
        'password1' etc. were identified/chosen.
    ]
"""




"""
19. Checking for valid form data
    & rendering a Message

##
# form.is_valid() 
##

Update the register() code as follows...
"""
def register(request):
    if request.method == "POST":                            
        form = UserCreationForm(request.POST) 
        if form.is_valid():                             #ADDED if-else: is_valid()    
            return render(request, 'users/register.html', {'msg':'Valid form!', 'form':form})
        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        #[Rob]
        # Send empty form object to be rendered with Django's form.as_p()
        form = UserCreationForm()
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )
"""

and add the following to the top of the  'register.html' template:

        {% if msg %}
            <p style="color:red;">Retrieved from render() - 'msg': {{msg}}</p>
        {% endif %}


- (Keep the '{% if form %}' block from the previous step below it)
   
   
   
#
#
TASK:
        Play with GET and POST request and try to get each of 
        the if-else path-ways above to execute
    
 
 
        
20. Saving a new user to the DB

##
# form.save() 
##

Below: adding form.save() can save the new user-data 
        from the form (POST request) as a new User 
        in the DB...

"""
def register(request):
    if request.method == "POST":                            
        form = UserCreationForm(request.POST) 
        if form.is_valid():  
            form.save()                                 #1. Add save() and 2. update 'msg' below
            return render(request, 'users/register.html', {'msg':'User created in DB!', 'form':form})
        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        #[Rob]
        # Send empty form object to be rendered with Django's form.as_p()
        form = UserCreationForm()
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )
"""

Re-visit 
    /register
see GET Request message
observe the DB.auth_user table in SQLiteStudio
Enter something like...
    Username:   testsave, 
    Password:   1234test, 
    Password:   1234test 
    
    & 'Sign-Up' (/Submit)
    
review the DB.auth_user and see the new user has been created
observe the msg displayed... 
  'User created in DB!'




##
# 20.1 form.cleaned_data example
##
Below we're adding a call to form.cleaned_data 
to get a 'cleaned' version of the data entered by the user
and adding this to the msg to show what User had been created...
"""
def register(request):
    if request.method == "POST":                            
        form = UserCreationForm(request.POST) 
        if form.is_valid():  
            form.save()                                 
            username = form.cleaned_data.get('username')    #1. Add cleaned_data() and 2. update 'msg' below
            return render(request, 'users/register.html', {'msg':f'Account created for {username}!', 'form':form})
        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        #[Rob]
        # Send empty form object to be rendered with Django's form.as_p()
        form = UserCreationForm()
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )
"""

Again:
Re-visit /register
see GET Request message
observe the DB.auth_user in SQLiteStudio
Enter something like...
    Username:   testclean, 
    Password:   1234test, 
    Password:   1234test 
    
    & 'Sign-Up' (/Submit)
    
review the DB.auth_user and see the new user has been created
observe the msg displayed... 
  Account created for testclean!

    (as per the if msg above)



#
# [Rob]
21. Create a flash message and re-direct to home. 

In views.py import messages with the following
"""
from django.contrib import messages
"""

update the import to include redirect
"""
from django.shortcuts import render, redirect           #Added ', redirect'
"""

update 'views.py'
Change the 
    if form.is_valid():
        
code-block to add a 'success' message and redirect to home...

"""
# ...
if form.is_valid():
    form.save()
    username = form.cleaned_data.get('username')
    #BELOW: 
    #   ADDED: message.success() & redirect 
    messages.success(request, f'Account created for {username}!')
    return redirect('blog-home')

"""

The views.py should then contain:
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":                            
        form = UserCreationForm(request.POST) 
        if form.is_valid():  
            form.save()                                 
            username = form.cleaned_data.get('username')    
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        form = UserCreationForm()
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )

"""
Again:
Save all files & re-visit 
    /register
Observe the - GET Request message
Observe the DB.auth_user in SQLiteStudio (no new user yet)
Enter something like...
    Username:   testmessage1, 
    Password:   1234test, 
    Password:   1234test 
    
    & 'Sign-Up' (/Submit)
    
review the DB.auth_user and see the new user has been created

[** Notice however that you don't see the message from:

        f"Account created for {username}"

    being displayed.]


#
#
21.1
    We didn't see the 'flash' message.success() because the 'blog-home'
    has no Django Template code to access and display it....
    
    
21.2. Update blog -> templates -> blog -> base.html 

    Update this part:
    <main role="main" class="container">
        <div class="row">
            <div class="col-md-8">
            
                {% block content %}{% endblock %}
                
            </div>
            ...
            
            
    with Django template code to display the messages...

    <main role="main" class="container">
        <div class="row">
            <div class="col-md-8">
            {#ADD HERE#}
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }}">
                        {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {#TO HERE#}
                {% block content %}{% endblock %}
            </div>
            ...
            

Save all code
Re-visit 
    /register
    
& you should see the message display for
  for the code above...

[Note: The flash message is only a one time alert. 
        When you refresh the home page it will be removed.]



[Above, if Django sees flash messages sent into the template we can loop over the messages
and print out each flash message. The <div> is using BootStrap Classes for styling.
This part alert-{{ message.tags } is grabbing the message tag. {{ message }} will 
display the message.]

Updated base.html (full-file)...


    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>

        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

        <link rel="stylesheet" type="text/css" href="{% static 'blog/main.css' %}">

        {% if title %}
            <title>Django Blog - {{ title }}</title>
        {% else %}
            <title>Django Blog</title>
        {% endif %}
    </head>
    <body>
        <header class="site-header">
          <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
            <div class="container">
              <a class="navbar-brand mr-4" href="{% url 'blog-home' %}">Django Blog</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarToggle">
                <div class="navbar-nav mr-auto">
                  <a class="nav-item nav-link" href="{% url 'blog-home' %}">Home</a>
                  <a class="nav-item nav-link" href="{% url 'blog-about' %}">About</a>
                </div>
                <!-- Navbar Right Side -->
                <div class="navbar-nav">
                  <a class="nav-item nav-link" href="#">Login</a>
                  <a class="nav-item nav-link" href="#">Register</a>
                </div>
              </div>
            </div>
          </nav>
        </header>
        <main role="main" class="container">
          <div class="row">
            <div class="col-md-8">
              {% if messages %}
                {% for message in messages %}
                  <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                  </div>
                {% endfor %}
              {% endif %}
              {% block content %}{% endblock %}
            </div>
            <div class="col-md-4">
              <div class="content-section">
                <h3>Our Sidebar</h3>
                <p class='text-muted'>You can put any information here you'd like.
                  <ul class="list-group">
                    <li class="list-group-item list-group-item-light">Latest Posts</li>
                    <li class="list-group-item list-group-item-light">Announcements</li>
                    <li class="list-group-item list-group-item-light">Calendars</li>
                    <li class="list-group-item list-group-item-light">etc</li>
                  </ul>
                </p>
              </div>
            </div>
          </div>
        </main>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
    </html>

#
#
[Rob-]



22. Check the admin page to see the new test users that have been created.

    http://127.0.0.1:8000/admin/
    
    Use the admin GUI to delete the test users created above.

#
#

23. Add an new email field to the UserCreationForm. To this we need to create a new file in
our users application directory. users -> forms.py 

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
    │       └── register.html
    ├── tests.py
    └── views.py


#
#

24. Inside forms.py import the following
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm #Inheritance Relationship

"""
forms               → gives you form fields like EmailField, CharField, etc.
User                → Django’s default user model (username, password...)
                        connected to auth_user DB table by default.
UserCreationForm    → pre-built form that already contains typical error 
                        messages, inputs, validation etc.

#
#

[Rob]
25. Create a class:
        UserRegistrationForm 
        
    with nested inner-class Meta. 

file: users/forms.py updated...
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

"""
[Rob]
-> class UserRegisterForm(UserCreationForm): 
    Inherit from the default UserCreationForm class but customise it.
    i.e. 
        add field 'email'
        
    --> class Meta:
            model = User
             - Which model the form is connected to → User (django.contrib.auth)
            
            fields = ['username', 'email', 'password1', 'password2']
            - Which fields to include and the order of appearance in the form
#
#

[Rob]
26. Now we can use the UserRegiserForm instead of the UserCreationFrom in our view.

See changes to 
views.py

in comments below...

Update the code in views.py to the following...
"""

from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm     #REMOVE:
from .forms import UserRegisterForm                         #CHANGE: Use new UserRegisterForm class
from django.contrib import messages                             

# Create your views here.
def register(request):
    if request.method == "POST":                            
        form = UserRegisterForm(request.POST)               #CHANGE: 
        if form.is_valid():  
            form.save()         
            username = form.cleaned_data.get('username')    
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')


        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        form = UserRegisterForm()                           #CHANGE:
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )
"""

#
#

27. Update the styling of the form. 

We could add Bootstrap classes to forms.py but this is mixing the presentation layer with
the back-end logic. A better approach is to use a third party Django app named crispy forms. 
This allows you to use some simple tags for styling. 
Crispy forms works with multiple CSS frameworks.

Install crispyforms
--> pip install django-crispy-forms
--> pip install crispy-bootstrap5

At this point we need to tell Django that this is an installed app.

Refer to https://django-crispy-forms.readthedocs.io/en/latest/

#
#

28. Open settings.py from django_project

django_project
│  ├── __init__.py
│  ├── asgi.py
│  ├── settings.py
│  ├── urls.py
│  └── wsgi.py

Update the INSTALLED APPS list to the following...
"""

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "users.apps.UsersConfig",
    "crispy_forms",             #ADDED
    "crispy_bootstrap5",        #ADDED
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

#At the bottom of settings.py specify the version of Bootstrap you want crispy forms to use.

CRISPY_TEMPLATE_PACK = 'bootstrap5'         #ADDED: new line

"""

#
#

28. Load crispy forms into the register.html template.

Updated register.html below

{% extends "blog/base.html" %}
{% load crispy_forms_tags %}                    <!-- ADDED -->
{% block content %}
        {% if msg %}
            <p style="color:red;">Retrieved from render() - 'msg': {{msg}}</p>
        {% endif %}

        {% if form %}
            <ul style="color:orange;">
                <p>Retrieved from render() - 'form' </p>
                <li>form.username: {{form.data.username}}</li>
                <li>form.password1: {{form.data.password1}}</li>
                <li>form.password2: {{form.data.password2}}</li>
            </ul>
        {% endif %}
        
        <div class="content-section">
            <form method="POST">  
                {% csrf_token %}
                <fieldset class="form-group">
                    <legend class="border-bottom mb-4">Join Here</legend>
                        {{ form|crispy }}               <!-- UPDATED:  let crispy take care of the formmating -->
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

29. Run development server and reload the register form.

--> python manage.py runserver  
--> Go to http://127.0.0.1:8000/register
Notice the updated styling on the form

--> View page source and notice the Bootstrap classes added to the form for styling


<fieldset class="form-group">
    <legend class="border-bottom mb-4">Join Here</legend>


    <div id="div_id_username" class="mb-3"> <label for="id_username" class="form-label requiredField">
            Username<span class="asteriskField">*</span> </label> <input type="text" name="username" maxlength="150"
            autofocus class="textinput form-control" required aria-describedby="id_username_helptext" id="id_username">
        <div id="id_username_helptext" class="form-text">Required. 150 characters or fewer. Letters, digits and
            @/./+/-/_ only.</div>
    </div>
    <div id="div_id_email" class="mb-3"> <label for="id_email" class="form-label requiredField">
            Email<span class="asteriskField">*</span> </label> <input type="email" name="email" maxlength="320"
            class="emailinput form-control" required id="id_email"> </div>
    <div id="div_id_password1" class="mb-3"> <label for="id_password1" class="form-label requiredField">
            Password<span class="asteriskField">*</span> </label> <input type="password" name="password1"
            autocomplete="new-password" class="passwordinput form-control" required
            aria-describedby="id_password1_helptext" id="id_password1">
        <div id="id_password1_helptext" class="form-text">
            <ul>
                <li>Your password can’t be too similar to your other personal information.</li>
                <li>Your password must contain at least 8 characters.</li>
                <li>Your password can’t be a commonly used password.</li>
                <li>Your password can’t be entirely numeric.</li>
            </ul>
        </div>
    </div>
    <div id="div_id_password2" class="mb-3"> <label for="id_password2" class="form-label requiredField">
            Password confirmation<span class="asteriskField">*</span> </label> <input type="password" name="password2"
            autocomplete="new-password" class="passwordinput form-control" required
            aria-describedby="id_password2_helptext" id="id_password2">
        <div id="id_password2_helptext" class="form-text">Enter the same password as before, for verification.</div>
    </div>
    <!-- UPDATED:  let crispy take care of the formmating -->
    
    
The styles are implemented with the default out of the box crispy form tag.

#
#

30. Fill out some test forms and notice the feedback given to the user is much clearer. 
At this point the form is styled nicely and gives clear user validation feedback.   

"""

        
    
    

    
    









