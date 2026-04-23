from django.shortcuts import render
from django.http import HttpResponse
from .models import Post



# Create your views here.

def home(request):
        # 'posts': posts,
    context_dict={
        'posts': Post.objects.all(),
        'title': 'rob-title'
    }
    return render(request, 'blog/home.html', context_dict)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})