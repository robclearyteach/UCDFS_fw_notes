"""
Unit 8 Walk through 
User Profile Information and Picture 

The default Django model for users does not provide a field for a 
profile picture. 
In order to do this we can extend the user model and create a new
profile model with a 1 - 1 relationship with a user. This means
1 user can have 1 profile picture and 1 profile picture will be associated with 1 user.

# 
# 

1. Create a new model inside models.py of the users app.

 users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    ├── models.py                   # HERE
    ├── templates
    │   └── users
    │       ├── login.html
    │       ├── logout.html
    │       ├── profile.html
    │       └── register.html
    ├── tests.py
    └── views.py

#
#

 2. Import the User model in models.py
"""
from django.contrib.auth.models import User

"""

 #
 #

 3. Create a Profile class and 1 to 1 relationship.
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
"""

[Rob]
Notice we have specified: 
 on_delete=models.CASCADE 
 
This means that if a User is deleted, the delete 'cascades' to 
  delete the related Profile.

 #
 #

 4. Add a profile picture field.
"""
image = models.ImageField(default='default.jpg', upload_to='profile_pics')
"""
 -> The first argument will be a default image for the user: default='default.jpg'
 -> The second argument is the directory where images will be uploaded to: upload_to='profile_pics'

#
#

[Rob]
5. Add a __str__() method to display a human-readable version of the Profile 
        (we keep it very simple for now)
"""
  def __str__(self):
        return f'{self.user.username} Profile'

"""

#
#

6. users -> models.py will now have the following code.
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
 """

 #
 #

 7. We have updated the model(s) for the Django project so 
    we need to 
        - makemigrations and
        - migrate
        
    [Notice: currently users/migrations/ has no 000x migration file]
    
    
#
#

8. Run the following from the CLI.
-> python manage.py makemigrations

Note the following error...

SystemCheckError: System check identified some issues:

ERRORS:
users.Profile.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".

-> Pillow is a Python library for handling images. Install it to use models.ImageField above.

#
#

9. Install Pillow

-> pip install Pillow

#
#

10. Make migrations

-> python manage.py makemigrations

This time you will see...

Migrations for 'users':
  users/migrations/0001_initial.py
    - Create model Profile  


[Rob]
Open up and view the 0001_initial.py file created.
Observe its similarity to the 'class Profile' from models.py

[Notice: this hasn't changed the DB yet 
        (open the DB in SQLiteStudio and see 'BlogPost'
          is the only non-Django table yet.)]

#
#

11. Run migrate

-> python manage.py migrate 

Output...

Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions, users
Running migrations:
  Applying users.0001_initial... OK


[Refresh the DB and view the 'users_profile' table has been created.]


#
#

[Rob]
12. In order to use the Django /admin page to manage Profiles, 
    we can register this model in the users/admin.py.

Open admin.py from the users app.

users
    ├── __init__.py
    ├── admin.py                # HERE
    ├── apps.py
    ├── forms.py
    ...

-> Update admin.py 
-> To the following...
"""
from django.contrib import admin
from . models import Profile

# Register your models here.
admin.site.register(Profile)
"""
#
#

13. Run the development server log-in to the /admin to see
    Profiles can be managed here now.

[Notice the 
========
Users
========
  Profiles
  
section now appears
]

14. Create some profiles using the Django /admin page 

-> python manage.py runserver
-> Go to http://127.0.0.1:8000/admin

14.1) Create a Profile with a profile_pic

-> Click Add Profile ( + Add ).
-> From the User drop down select a user.
-> Select Choose File and upload an image.
-> Then SAVE

[*Notice: a new profile_pics/ subfolder 
          has been created and the profile_pic 
          that was uploaded was copied in there.]

-  Visit the new profile_pics/ subfolder for your django project

14.2) Create a Profile without a profile_pic

-> Repeat the steps above for another user but this time
    *do not* upload an image 
    (so that he default image can be used/tested).


[** Make a note of the usernames that you 
    have created Profiles for 
    (needed for the next step).           
]
    
    
#
#

15. Test User profile access using Django ORM.

-> run python manage.py shell

-> Import the Django built in user model:

  >>> from django.contrib.auth.models import User


15.1: Select the User that you created a Profile for
      (the one with the profile_pic)

  >>> user = User.objects.filter(username='blackpanther').first()
  >>> user
  <User: blackpanther>>

#
#

15.2: Access the profile associated with the user and the image

>>> user.profile
<Profile: blackpanther Profile>

>>> user.profile.image
<ImageFieldFile: profile_pics/profile_img_filename.png>
    
#
#

15.3: Experiment with Access to image attributes 
        width, height, size for example

>>> user.profile.image.width
4024
>>> user.profile.image.height
4220
>>> user.profile.image.size
15656170

#
#

15.4: Experiment with access to a user profiles image location
>>> user.profile.image.url
'/profile_pics/profile_img_filename.png'


15.5: Experiment to see the profile image location if no image
        is uploaded (default.jpg)

>>> user = User.objects.filter(username='pinkpanther').first()
>>> user.profile.image.url
'/default.jpg'

[Note: we haven't stored a 'default.jpg' image yet but we'll 
        do that soon].

15.6: -> Exit the shell 
>>> exit()




#
#
[Rob]
16. Define MEDIA_ROOT and MEDIA_URL

Currently the location of profile_pics/ folder is the under the 
project root (same as Django apps: e.g. blog/, user/ etc.)
It is generally better to configure a separate folder 'media/' 
for storing uploaded/user content

├── blog
├── db.sqlite3
├── django_project   
├── manage.py
x x x x x x x x x x
├── profile_pics                            #better to move to 'media/'
x x x x x x x x x x
└── users


-> Open mysite/settings.py

Add these lines to the end of settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



17. Next:

-> Go to http://127.0.0.1:8000/admin/
-> Select Profiles
-> Select the user with a profile_pic from earlier
-> Re-upload the same profile_pic
-> click SAVE

**Notice: Django has now created a
            'media/' folder with a new
            'profile_pics/' sub-folder inside.
            
            Uploaded files will now be stored here.

├── djangoproject
│   ├── media                   # CREATED
|   |   |--profile_pics/        # CREATED


#
#


    
18. Open django shell again:

python manage.py shell

>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username='pinkpanther').first()
>>> user.profile.image.url
                                    #what location?
>>> exit()


19. Then in the Django /admin page

    Select the other user (without a profile_pic): e.g. 
        pinkpanther_Profile
        
        to view the Django Admin view of their Profile.
    
    Click SAVE (without making a change).

repeat the shell experiment above:

python manage.py shell

>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username='pinkpanther').first()
>>> user.profile.image.url
'/media/default.jpg'
#
#

20. Delete the original profile_pics/ directory, as files 
    are now managed via MEDIA_ROOT and served through MEDIA_URL.

├── mysite
├── media
│   └── profile_pics                        # KEEP
│       └── your_file_name.jpeg
...
x x x x x x x x x x x x                     # DELETE
├── profile_pics                            #  Now exists under 'media/'
│   ├── your_file_name.jpeg
│   └── your_file_name_zny5S4O.jpeg
x x x x x x x x x x x x

├── db.sqlite3
├── manage.py


#
#

[Rob]
Currently we have 
    - created a 'Profile' model, 
    - migrated it to the DB ('user_profile' table)
    - linked to User table ('auth_user' <--> 'user_profile')
    
But we have been using the Django Admin (/admin) UI
    to 
        - create profiles
        - view profiles
        - update (add images) profiles
        
        
        
23. NEXT: We want to enable 
        that functionality in our Blog App.
        i.e. 
            A user can Login and view their
            Profile (with profile_pic) 



##
# TASK:
##
Recall /profile :
	- where is the code to serve this?
    - what is it currently serving?
	- where in this Blog App (Django Project) is it
        that a user can trigger the code to serve a Profile view?
    - can you give a walkthrough of how Django does that?
  
  
  
  
23: To add 'Profile' functionality to our Django Blog App  
        
    Not only do we need to: 
    
    =       add template code to users/profile.html 
            to render the Profile-page with profile_pic and user details
            
    we also need to...
    
    =       add media (static file) handling to mysite/urls.py 
 
        * For more on why we add static (media) handling...
        https://docs.djangoproject.com/en/6.0/howto/static-files/#serving-static-files-during-development
        https://docs.djangoproject.com/en/6.0/howto/static-files/    
#
#
    
23.1: Add media (static file) handling to mysite/urls.py.

    Go to mysite/urls.py 

    a) ADD these imports

    from django.conf import settings
    from django.conf.urls.static import static

    b) then after urlpatterns...

    urlpatterns = [
        #...
    ]

    ADD:

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        

    Your mysite/urls.py should then look like this:
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls') ),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/',  auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""

#
#
23.2 Add template code to users/profile.html 
            to render the Profile-page with profile_pic and user details


 users
    ...
    ├── templates
    │   └── users
    │       ├── login.html
    │       ├── logout.html
    │       ├── profile.html            # HERE
    │       └── register.html
    ...

-> Update the file with the following template code...



{% extends "blog/base.html" %}

{% block content %}
    <div class="content-section">
        <div class="media">
            <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
            <div class="media-body">
                <h2 class="account-heading">{{ user.username }}</h2>
                <p class="text-secondary">{{ user.email }}</p>
            </div>
        </div>
    </div>
{% endblock content %}




#
#

[Rob]
24. View the Profile page...

-> Login with (the user that has a profile_pic).
-> Click the 'Profile' link from the nav-bar (or visit /profile)

-> You should see a profile page with a profile_pic, username and email.

#
#




25. 
    For user profiles where no image was uploaded:
    we want a default image to display.
    
    
25.1: Get and save a default profile_pic 
        to the media/ folder (see folder structure below): 

e.g. Get image from somewhere like...
    https://openclipart.org/image/800px/247320

[right-click, save image as...]

django_project
...
├── media
│   ├── default.jpg                             # Save here as 'default.jpg'
│   └── profile_pics
│       └── other_profile_pic.jpeg


[*Note: if you have a .png ('default.png' for example), instead of a .jpg
    just rename the file to media/default.jpg (after saving it) for a quick fix.
]


25.2
 Login with (the user that doesn't have a profile_pic) and 
 go to the Profile (/profile) page: you should see the default
 image now....







#
#
[Rob]
26. Auto create a profile when a new user is created.

Currently when a new user registers we have been
logging-in to the Django Admin page (/admin) 
and create a profile manually.

We want the Blog site create a Profile page 
automatically when a new user registers. 


26.1: TASK: precursor
 
        run a django shell 
        
        See if you can  use shell commands to simulate 

            - a new user being created
            - an associated profile being created for that user
            - ensure user & profile are .save()'d and visible in the DB
            

    [HELP:  re-visit the Unit_05_Walkthrough file to see shell commands used there
            re-visit above: 'Test User profile access using Django ORM.'
                                to see shell commands used there
                                
        See recommended commands below to handle TASK:
        >>> newuser = User.objects.create_user('newuser1', password='1111test')
        >>> newuser
        >>> newuser.profile
        >>> Profile.objects.create(user=newuser)
        >>> user.profile
        
        For more: 
                    https://docs.djangoproject.com/en/6.0/topics/db/queries/
        ]
"""

[Rob]

"""
27.: So to get Django to do this automatically for each new User
     registration...

Inside the user app create a file called users/signals.py

users
...
    ├── models.py
    
    ├── signals.py                      # Create  
   
    ├── templates
    ├── tests.py
    └── views.py

#
#
[Rob]
27.1: Add the following code to signals.py
"""
# below: Django 'post_save' event
#        post meaning 'after' save: 
#           - event fires every time .save() is called on a model instance.
#
#   @receiver(post_save, sender=User)
#   -narrows it to when User.save() occurs
#
from django.db.models.signals import post_save      
from django.contrib.auth.models import User         
from django.dispatch import receiver                
from .models import Profile                         

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()

"""
Functions explained below.

A signal is Django’s way of saying:

“Hey, something just happened — how to react to it?”

For this case:

Event: a new user registers: a User object is created ( User model object .save() )
Reaction: automatically create a matching Profile


Above: 
@receiver(post_save, sender=User)
    - “Run this function whenever a User is saved”

# create_profile()
#

instance
    - The actual user that was just saved

created
    - True only when a new user is created (not updated)

Profile.objects.create(user=instance)
    - Creates a profile linked to that user


# save_profile()
#
instance.profile.save()
    - As the signal's 'sender=User'
    -    the signal's 'instance' refers to 
            the particular 'user' (i.e. the one .save() was called on).

[Rob-]
"""


#
#
"""
27.2: Import signals into users/apps.py --> ready() function

 users
    ├── apps.py             # Open.
...
#
#

27.3. Update 'users/apps.py' to include the following 
        'ready()' function.
"""
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "users"

    def ready(self):                #ADDED
        import users.signals        #HERE: imports signals.py 

"""
[Rob-]

#
#

27.4. Test the changes.

-> Register a new user using the website.
-> Log in to the new account.
-> Go to the profile page.

At this point you should see the the new user account with the default image.

"""











