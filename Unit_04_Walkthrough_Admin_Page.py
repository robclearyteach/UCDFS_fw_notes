"""
Unit 4 Walk through 
Admin Page 
Now we will learn how to access the admin page of the site.
We can use this to see what is on the site and also use a
friendly GUI for CRUD.

# 
# 

1. Run your application with python manage.py runserver. Navigate to http://127.0.0.1:8000/admin

From here you will see the login page but at the moment it cannot be used as there are no default
credentials.



#
#

2. Create a user for admin.

[Rob]
From the command line stop the development server with ctrl + c
In the command line type:

python manage.py createsuperuser

    When you run this command you will likely get long error message.
    The last line as shown below points to the problem. 

        ...
        django.db.utils.OperationalError: no such table: auth_user



#
# 
# [HERE: useful to open/connect-to the project/db.sqlite3 database file
#        (e.g. using  SQLiteStudio). 
#		  [See no tables]
#		  [RECALL: the 'runserver' cmd created an empty 'db.sqlite3'.]


[Rob-remove]

#
#

In the command line type: 
    python manage.py migrate


Produces Output like...

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK



This 'migrate' command has run through the:
    project/mysite/settings.py
    --> 
        INSTALLED_APPS = [ 
            'blog.apps.BlogConfig'
            'django.contrib.admin', 
            'django.contrib.auth', 
            'django.contrib.contenttypes', 
            'django.contrib.sessions', 
            'django.contrib.messages', 
            'django.contrib.staticfiles', 
        ]
        
    and caused certain DB ('db.sqlite3') tables to be created.

Such as auth_user (from the earlier 'createsuperuser' command error).


# [If possible: open/connect/refresh the db.sqlite3 (e.g. SQLiteStudio)
#               and see DB tables (auth_user etc) now created.]


# NOW we can re-run the earlier createsuperuser command 

In the command line type:
    python manage.py createsuperuser


Add in the details asked for example

    Username: admin
    Email address: test@test.com
    Password: test
    Password (again): test
    This password is too short. It must contain at least 8 characters.
    Bypass password validation and create user anyway? [y/N]: 
    Superuser created successfully.


# [ Note: when entering the password above 
#           what you enter is not displayed. 
#           Press Enter after anyway.]

# [ Note: option to bypass a short password can be useful for testing.

#
#





##
3. Run:

python manage.py runserver

Navigate to http://127.0.0.1:8000/admin

Login with your username and password.
You can now see the Django administration page.





#
#

4. The admin page allows us to do a lot on the back-end. As a quick example navigate to the Users
folder and navigate to the current user you have created.

Note the encryption the Django has provided on your password. Django is not storing your plain text
password it is applying the encryption for you.

    Username:
    admin
    Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.

    Password:
    algorithm: pbkdf2_sha256 iterations: 600000 salt: 5yas5L**************** hash: r8q0qq**************************************
    Raw passwords are not stored, so there is no way to see this user’s password, but you can change the password using this form.

#
#

5. Show example of creating a new user from the GUI. Talk through the GUI.


Django Admin:

#User       +Add

[Save]

#Notice url: something like...
--> admin/auth/user/2/change/


#Permissions

[] Active
[] Staff Status
[] Superuser Status

#Groups

#Permissions


"""







