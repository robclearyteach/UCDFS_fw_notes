from django.shortcuts import render
from django.http import HttpResponse


list_of_posts = [
    {
        "author": "Bill Tutman",
        "title": "Getting Started with Django",
        "content": "A django basics and understandings post.",
        "date_posted": "05/02/2026"
    },

    {
        "author": "Djan Gu",
        "title": "Don't forget the django tutorial",
        "content": "Exploring frameworks like django post.",
        "date_posted": "18/03/2026"
    }
]



# Create your views here.

#blog/templates/blog/home.html => blog/home.html
def home(request):
    context_dict={
        'posts':list_of_posts,
        'title':'homeXX'
    }
    return render(request, 'blog/home.html', context_dict)

def about(request):
    return render(request, 'blog/about.html', {'title':'rob'})

def me(request):
    return render(request, 'blog/me.html')