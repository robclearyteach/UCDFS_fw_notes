"""
Unit 13 Walk through 
Password Reset
[Rob]
     Django has built in functionality to support a 
     'Forgot your password?'
     email reset process. 

# 
# 

1. Open Django Project urls.py. 
 mysite/urls.py


In urlpatterns add the following...
"""
from django.contrib.auth import views as auth_views
#...
urlpatterns = [
    #...,
path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
]

"""

#TASK:
What does each part of the above path() do?









#
#

2. Next, create the template 'users/password_reset.html'

--> Create a new file in the templates folder of the 'users' app
    (i.e. we are viewing the password reset process as 'User' logic)
    
-> users/templates/users/password_reset.html

[├── templates
│   └── users
│       ├── login.html
│       ├── logout.html
│       ├── password_reset.html             #ADDED
│       ├── profile.html
│       └── register.html]




3. Add the following form to password_reset.html


#
#

{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Reset Password</legend>
                {{ form|crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Request Password Reset</button>
            </div>
        </form>
    </div>
{% endblock content %}


[Rob-]
#TASK: 
# What is 'form' above and where does it come from?
# (Ans below: try to answer the TASK on your own first
#               before peaking below...) 



















# TASK: answer:
#   The 'form' in the 'password_reset.html' template
#   is a Django form instance specifically a 'PasswordResetForm' 
#   (from django.contrib.auth.forms).
#
#   the mysite/urls.py 
#       path( ... auth_views.PasswordResetView.as_view(template_name='...', ...)
#   delegates the display/view of '.../password-reset/' to this class-based view.
#   It has (or "contains") the form instance which the template can refer to as 'form'.


#
#

4. If we tested this change alone we'd get an error as 
    Django requires a redirect after submitting that form
    (after entering an email-address for the password-reset).
    
    Let's define that next...

    Again: mysite/urls.py 
        ADD a path for the redirect to the end of the urlpatterns list:
"""
from django.contrib.auth import views as auth_views
#...
urlpatterns = [
    #...,
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
]
"""
[Rob-
#
#

5. 
    And set up a HTML template for the redirect display...
    
    --> Create a new file: users/templates/users/password_reset_done.html
[Rob-]

#
#

6. Add the following HTML and save:

{% extends "blog/base.html" %}
{% block content %}
    <div class="alert alert-info">
        An email has been sent with instructions to reset your password
    </div>
{% endblock content %}


#
#

[NOTE: Inside the content block:

    The <div> element with a class of alert alert-info, 
    is a Bootstrap class to display like a flash-message...

[Rob-]
#
#


7. Test what we have created so far. 
[Rob]

# 7.1
--> Run the development Server
--> Visit: 
    http://127.0.0.1:8000/password-reset/
--> You will see the Rest Password page with a single email field.
--> Add a test email 
    [NOTE: choose an email that is NOT in your app's db)
        e.g. 
            test@test.com 
            
--> select 'Request password Reset'

You will likely see a redirect to:
    .../password-reset/done/

showing the message from the template ('password-reset-done.html'):

"An email has been sent with instructions to reset your password "


[Rob]
What's happening here?
    - The Form is submitted
    - Django checks:
        “Does this email exist?”
        -   If NOT found:
            Django’s PasswordResetView runs form.save() and then automatically redirects
            to 
                .../password-reset/done/

No email was actually sent. This simulation above
can serve to show how django behaves if a non-existing 
user email is entered.
The default behaviour prevents attackers from checking 
which emails are registered (user enumeration protection)


 
 
# 7.2  
[Rob]
Let's test with an existing user email now:
--> Re-Visit: 
    http://127.0.0.1:8000/password-reset/

--> Add an email (IN your app's db)
        e.g. 
        black@panther.com 
        
        (for the case that email is in your db)
        
--> select 'Request password Reset'


--> See a Django error-page is displayed

        
This time, the entered email was checked
against the DB model (User.objects.filter(email=...)).

In the browser traceback, line 6 shows:

{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}

Here Django was trying to build the password reset link that 
would be included in an email to the user.
The problem is that we have not yet defined a URL pattern named 
    password_reset_confirm, 

so Django cannot generate the link and raises a NoReverseMatch error.

Breaking it down:

- {{ protocol }}                         → inserts http or https
- {{ domain }}                           → inserts your site's domain name
- {% url 'password_reset_confirm'...}    → generate a pasword reset link

Django also passes two arguments to that URL:

    % url 'password_reset_confirm' uidb64=uid token=token %}

        - uidb64    → the user's ID encoded in base64
        - token     → a secure password reset token

These values uniquely identify the user and verify that the password reset request is valid.



 #
 #

[Rob-]
 8. Add the route...
        ADD a path for the generated reset-link 
        to the end of the urlpatterns list:
        
    Again: mysite/urls.py 
"""
from django.contrib.auth import views as auth_views
#...
urlpatterns = [
    #...,
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),	name="password_reset_confirm"),
]
"""
#
#

9.  Add the HTML template...

--> Create a new file:
         users/templates/users/password_reset_confirm.html

[Rob-]


{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Reset Password</legend>
                {{ form|crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Reset Password</button>
            </div>
        </form>
    </div>
{% endblock content %}

[Rob-]

#
#

10. Re-test: in the development server. 

--> Re-Visit: 
    http://127.0.0.1:8000/password-reset/

--> Add the email 
        [NOTE: and email IN your app's db this time]
        e.g. 
            black@panther.com 
        
            (for the case that email is in your db)
        
--> select 'Request password Reset'

--> You may see the:
    .../password-reset/done 
    
    page 
    

BUT: 
Observe:
    Server Logs: 
    Error:
    
"""
# Failed to send password reset email to 18 ...
#   Traceback...
#        ...email_message.send()
#    
#   ConnectionRefusedError: ... No connection could be made because the target machine actively refused it   
"""    

Observe:
    Server Logs: 
"POST /password-reset/      HTTP/1.1" 302 0
"GET  /password-reset/done/ HTTP/1.1" 200 
    
--> Note the error 'ConnectionRefusedError at /password-reset/'


11.
##
# Before proceeding: 
#   Set up a Gmail account for testing
#

We will recommend a Gmail account for testing. 
If you do not have a Gmail account you will
need to create one for the following steps.

11.1
##
# Create a test Gmail account:
#   e.g. 

    myburnergmailtest123@gmail.com

11.1.1
        ##
        # Se up 2-factor authentication 
        #   for that e-mail account
        #   [NOTE: this is required: see link:
        #       https://support.google.com/accounts/answer/185839  
        #   ]

        ==    Open the Google Account for that email.
        #i.e.
        #
        # In Gmail Inbox view: 
        #       see the dot-matrix (dice icon)
        #       in the top-right corner
        #   Press that and choose the:
        #       'Account' (with profile-icon) 
        #       (top-left of the drop-down).ascii

        ==    Go to 'Security & sign-in'.   
        #   In the managment pane on the left

        ==    “How you sign in to Google,” 
        #   Middle section

        ==  select Turn on 2-Step Verification.


        == Log out, log back in
        == [Optional: check "[] Don't ask again on this device"]


11.2
Set up use "App Passwords" on that Gmail account. Details at the link below.
    https://support.google.com/accounts/answer/185833?hl=en



        # To Set up "App Passwords" 
        #   1. log-in
        #   2. visit: https://myaccount.google.com/apppasswords
        #   3. See
                    <- App passwords (page)
        #   4. Choose '+' (or ADD) 
        #       (Enter a name for your app...)
                    
                    ucdpa-2507-fw-unit14
                
        #   5. *click (Create) 

        #   6. See:
                Your app password for your device:
                e.g.
                
                    abcd dcba ppoo yynn

                #copy-paste and keep secure

##
#
==============
links above for review:
==============
https://support.google.com/accounts/answer/185833?hl=en
https://support.google.com/accounts/answer/185839
#
##




12.
##
# Select a user in your App's DB as 
#   a 'test-user'
# Set the 'test-user' email to the newly set email address:

# ONE WAY: 
#   directly change the test-db
# 
# In SQLiteStudio (or similar)

UPDATE auth_user
    SET 
        email = 'myburnergmailtest123@gmail.com'
    WHERE 
        id = 18 ;

 
 #Verify the user was set:
 
    SELECT * FROM auth_user;
 
 
 
 
 
 
 
 
 
 
 
 
 
 
13. In django_project -> settings.py add the following...

"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True											#Transport Layer Security (like HTTP_S_]
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']  				# app email address
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']  		# app specific password 

"""





#
#

14. 
Test again:
[NOTE:
        * Use the newly created email address: e.g. 
                
                myburnergmailtest123@gmail.com

        * Recall: one user in the App DB 
                has now had it's email field 
                set to this address. 
]

# 14.1.
        
--> Re-Visit: 
    http://127.0.0.1:8000/password-reset/

--> Add the newly created email address:

        myburnergmailtest123@gmail.com

--> select 'Request password Reset'


--> You should see the URL redirected to:
http://127.0.0.1:8000/password-reset/done/

With the message...
-> An email has been sent with instructions to reset your password 



# 14.2.
    Check your test email and you should see 
    an email has arrived: 

    FROM:       myburnergmailtest123@gmail.com
    SUBJECT:    Password reset on 127.0.0.1:8000
    BODY:
    "
    You're receiving this email because you requested a password reset for your user account at 127.0.0.1:8000.
    Please go to the following page and choose a new password:
    http://127.0.0.1:8000/password-reset-confirm/MTI/bxh2ev-14ab751d3aa5a61fab7ca1688b939001/
    Your username, in case you’ve forgotten: blackpanther

    Thanks for using our site!
    The 127.0.0.1:8000 team
    "




15. Test the password-reset link...

Click on the link in the email: e.g. ...
-> http://127.0.0.1:8000/password-reset-confirm/MTI/bxh2ev-14ab751d3aa5a61fab7ca1688b939001/

[NOTE: the tokens are unique to the account email. 

        Related template code:

        {% url 'password_reset_confirm' uidb64=uid token=token %}

        Breakdown:

        MTI
        → the uidb64 value
        → base64-encoded user ID
        bxh2ev-14ab751d3aa5a61fab7ca1688b939001
        → the password reset token
        → used to verify the reset request is valid and secure

        Django inserts both values dynamically when generating the reset link
]


# Visiting the link in the email-body brings you to:

     http://127.0.0.1:8000/password-reset-confirm/MTI/set-password/

When you attempt to change the password you will receive an error as follows...

Exception Type:	NoReverseMatch
Exception Value: Reverse for 'password_reset_complete' not found. 'password_reset_complete' is not a valid view function or pattern name.


#
#

16. Add the route...
        ADD a path for the reset-complete 
        final landing page of the process 
        
    Again: mysite/urls.py 
"""
from django.contrib.auth import views as auth_views
#...
urlpatterns = [
    #...,
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
]
"""

#
#

17.  Create the HTML template:
[Rob-]

--> Create a new file: users/templates/users/password_reset_complete.html


Add the following HTML:

{% extends "blog/base.html" %}
{% block content %}
    <div class="alert alert-info">
        Your password has been set.
    </div>
    <a href="{% url 'login' %}">Sign In Here</a>
{% endblock content %}

[Rob-]
#
#

18. Add a link to the:
    main log-in page.
    
    This 'Forgot your password?' link
    will start off the reset password
    process from the route:
    
        password-reset/ 


19. 
--> Edit/update: users/login.html

[Rob-]

Add the following after the 'Login' <div>.
"""
<small class="text-muted ml-2">
  <a href="{% url 'password_reset' %}">Forgot Password?</a>
</small>
"""

For reference the full login.html file will be as below.

#
#

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
        
        {# <!-- ADDED 'small' block below --> #}
        <small class="text-muted ml-2">
            <a href="{% url 'password_reset' %}">Forgot Password?</a>
        </small>
        
        
    </form>
    
    <div class="border-top pt-3">
        <small class="text-muted">
            Need An Account? <a class="ml-2" href="{% url 'register' %}">Sign Up Now</a>
        </small>
    </div>
   
   </div>
{% endblock content %}



#
#

20. Visit the 'Login' link and 
    test the entire password-reset process
    from start to end.

--> Run the development server
--> Go to the login page.
--> Select the forgot password link
--> Request to change the password to the gmail account you have configured. 
--> Open your email
--> Click the reset password link
--> Reset the password 
--> Login again with the newly reset password
--> [Optionally: view the change in the DB]




##
[OPTIONAL TASK:
1. 
    Test this on both a local:
        - Postgres and
        - SQLite 
    DB. 
    
2.
# Render free-tier blocks SMTP:
    https://render.com/changelog/free-web-services-will-no-longer-allow-outbound-traffic-to-smtp-ports

]
"""




