from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Added import here
from django.views.decorators.cache import never_cache

from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm                         #CHANGE: forms.py->UserRegisterForm
from django.contrib import messages       

                      

# Create your views here.
def register(request):
    if request.method == "POST":                            
        form = UserRegisterForm(request.POST)               #CHANGE: 
        if form.is_valid():  
            form.save()         
            username = form.cleaned_data.get('username')    
            messages.success(request, f'Account created for {username}, now you can login.')
            return redirect('login')


        else:
            return render(request, 'users/register.html', {'msg':'INValid form!','form':form} )
    else:
        form = UserRegisterForm()                           #CHANGE:
        return render(request, 'users/register.html', {'msg':'GET Request','form':form} )
    
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
        u_form = UserUpdateForm(instance=request.user)              #instance passed
        p_form = ProfileUpdateForm(instance=request.user.profile)   #instance passed

    #Create a context dict to pass to the 'profile.html' template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context) #Context passed here