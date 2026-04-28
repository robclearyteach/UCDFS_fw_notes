"""
Unit 9 Walk through 
Update User Profile Information and Picture 

We'll be finishing up our user profile page and making it so that
users can update their information from this page and also upload a new profile
picture we're also going to set this up so that our images are automatically
resized when we upload them so that we don't have extremely large images on our
file system when we're only displaying the small little you know 200 pixel
images here on the profile.

# 
# 

1. Update User Profile by creating some more forms. 

    Open users -> forms.py

    users
        ├── __init__.py
    ...
        ├── forms.py                #OPEN
    ...

#
#

2. Create a form to update the user model. Update forms.py adding the following class.
This allows the user to update their username and email.

"""
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
"""
#
#

3. Create an additional form for updating the Profile picture. 
Add the following import statement to forms.py.
"""
from . models import Profile

"""

forms.py should now look like the following.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

"""

#
#

4. Create an additional form to update the profile image. Add the following class to forms.py.
"""
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image']
"""

We now need to add the forms we have created to the views.py. Open views.py in users.

#
#

5. Open users/views.py

 users
    ├── __init__.py
...
    └── views.py            #OPEN

#
#

6. In views.py we already have the UserRegisterForm as follows.
"""
from . forms import UserRegisterForm

"""
Add the UserUpdateForm and ProfileUpdateForm as follows.
"""
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

"""

#
#

7. Create instances of the forms inside the profile function in views.py. 
    Update the existing profile() function
    to the following...
"""
@login_required
@never_cache
def profile(request):
    u_form = UserUpdateForm() 
    p_form = ProfileUpdateForm()

    #Create a context dict to pass to the 'profile.html' template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context) #Context passed here
"""
#
#
[Rob]
8. Add the form to the current 'profile.html' template. 
   Add below the comment-line:
       <!-- FORM HERE -->
   
   (if you see it), or otherwise below the 
    the last closing div currently visible:
    
            <! -- put form here -->
        </div>
        {% endblock content %}     
        
[Rob-]            

<form method="POST" enctype="multipart/form-data">          
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Profile Info</legend>    
        
                {{ u_form|crispy }} 
                {{ p_form|crispy }} 
        </fieldset>

        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Update</button> 
        </div>
</form>



[Note: above: Added an encoding type: this is needed for file uploads (e.g., images). ]

#
#

11. Save all the files and run the server then go to the profile page.

--> python manage.py runserver
--> http://127.0.0.1:8000/profile/



#
#


[Rob]
12. 
Notice that the current Username and Email (values for current User) 
    are not showing in the <input> boxes from the forms. 
    
It would be better for them to see the current details when the form loads.

To do this we need to make some changes to users/views.py. Open views.py.

[Rob-]
users
    ...
    └── views.py        #OPEN

#
#

[Rob]
13. Update the current profile function to the following.
"""
@login_required
@never_cache
def profile(request):
    u_form = UserUpdateForm(instance=request.user)          #instance passed
    p_form = ProfileUpdateForm(instance=request.user.profile)    #instance passed

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

"""
[Rob-]
This small change will display the current details 




14.
    This new Profile display should result form a GET request.
    
    We can add an 
        if request.method == 'POST':
            # handle post request
            #   i.e. - after update of current user data
        else: 
            #handle get request
            # display current user data
    
    
    
Updated view below...
    ADDED the if-block code
"""
@login_required
@never_cache
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

"""

#
#

15. Let's give some feedback to our user letting them know that they've updated their profile.
    As per the register() view, we can use messages.success() and redirect()...

--> Full profile view below
"""
@login_required
@never_cache
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated') #ADDED
            return redirect('profile')                                  #ADDED
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
"""


[Rob]
Note that it is important to do a redirect here.

Use a redirect after handling a POST to follow the Post-Redirect-Get (PRG) pattern.

If you render the template directly after a POST, refreshing the page will resubmit 
the form (duplicate submissions + browser warning). 
A redirect converts the flow to a GET request, so refreshes are safe and don’t resend data.

More on Post Get Redirect here 
https://stackoverflow.com/questions/10827242/understanding-the-post-redirect-get-pattern

#
#

16. Test the changes. 

"""




