from django.shortcuts import render
from django.http import HttpResponse
from . models import Post

from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # ADDED
    context_object_name = 'posts'       # ADDED. term template can use 'posts'
    ordering = ['-date_posted']         #ADDED: order the posts from newest to oldest.


class PostDetailView(DetailView):
    model = Post
    
    
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