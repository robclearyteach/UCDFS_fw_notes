"""
Unit 1 Walk through
Django Installation 

0.
-->Install virtualenv using pip: "pip install virtualenv".
-->Create a virtual environment: "virtualenv your_env_name".
-->Activate the virtual environment:
    -->Windows: "your_env_name\Scripts\activate".
    -->macOS/Linux: "source your_env_name/bin/activate".   

# 
# 

1. Install Django inside the virtual environment:
pip install django

# 
# 

2. Confirm install
python -m django --version

# 
# 

3. Create project from scratch
We will now use some commands for Django as we have it installed

django-admin

The above will show available sub commands. For now we will use startproject.

# 
# 

4. django-admin startproject django_project


[ROB]
# view the created folder:
#.../django-project

# delete that folder

# regenerate with

4. django-admin startproject mysite django_project





The command above will create a Django project directory. The directory name will be
django_project. The name should be relevant to your project.

Show the directory structure either in Terminal/VS Code/Sublime etc. Talk through each of the
files. If on Mac a handy tool to view the tree structure can be installed with brew install tree.
More details here https://michaelsoolee.com/tree-tool/

# 
# 

5. tree from Terminal or open in Terminal/VS Code/Sublime etc.

├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

# 
# 

6. manage.py
manage.py is at the base level and allows us to run command line commands. 
We are not changing this file. Open file to show the contents.

# 
# 

7. django-project directory is also at the base level. Inside this we have 
five files. Show the contents of all.

# 
# 

8. init.py is empty. It tells Python that this is a python package.

# 
# 

9. setting.py we will use as we build our app. For now give a brief overview. Mention 
SECRET_KEY, DEBUG = TRUE, DATABASES etc

# 
# 

10. urls.py. This is where we set up the mapping for our url routes. Where we want the user to go.
At the moment we have the default admin route. Show in file.

urlpatterns = [
    path("admin/", admin.site.urls),
]

We will see how this works when we add more routes

# 
# 

11.wsgi.py and asgi.py. This is how are python web app and server communicate.
Django sets up a default configuration of these files.

WSGI is the main Python standard for communicating between web servers and applications, 
but it only supports synchronous code. ASGI is the new, asynchronous-friendly standard 
that will allow your Django site to use asynchronous Python features, and asynchronous 
Django features as they are developed.



[ROB]
12.a
# cd to the django_project/ 


12. python manage.py runserver
The command will run the basic web app. You will see something like the following.

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

July 11, 2023 - 12:44:54
Django version 4.2.3, using settings 'django_project.settings'
Starting development server at http://127.0.0.1:8000/
Run 'python manage.py migrate' to apply them.
Quit the server with CONTROL-C.

#
#

Note the warnings and the suggestion to remove them
Run 'python manage.py migrate' to apply them.

We will come back to this again

12. Access the default site at local host.
Starting development server at 
http://127.0.0.1:8000/ or localhost:8000

#
#

13. Navigate to http://localhost:8000/admin/
Open the urls.py file to show the url patterns

#
#

14. Show how to stop the server ctrl + c
Remind how to run the server. python manage.py runserver 

#
#


"""







