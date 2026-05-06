from django.shortcuts import render
from django.http import HttpResponse
from . models import Post

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from django.urls import reverse                                 # ADD

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url = '/blog/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    
         
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):       # Inherits from UpdateView & requires login.
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']   #gives the form Object for the template

    #Override form_valid() method 
    def form_valid(self, form):
        form.instance.author = self.request.user    # Set the author on the form
        return super().form_valid(form)             # Validate form by running form_valid method from parent class.
    
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # ADDED
    context_object_name = 'posts'       # ADDED. term template can use 'posts'
    ordering = ['-date_posted']         # ADDED: order the posts from newest to oldest.


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