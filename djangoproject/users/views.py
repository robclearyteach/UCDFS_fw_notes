from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm     #REMOVE:
from .forms import UserRegisterForm                         #CHANGE: forms.py->UserRegisterForm
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