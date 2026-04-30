"""
Unit 10 Walk through 
Posts Create Update Delete

Here we will learn how to perform CRUD operations in Django and learn the power of 
class based views. 

# 
# 

1. We are going to look at using class based views for displaying, updating and deleting new posts.
Within our blog app open views.py. So far we have used function based views.

--> Open blog -> views.py and should have the following.

"""
from django.shortcuts import render
from django.http import HttpResponse
from . models import Post

# Create your views here.x
def home(request):
        # 'posts': posts,
    context_dict={
        'posts': Post.objects.all(),
        'title': 'rob-title'
    }
    return render(request, 'blog/home.html', context_dict)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

"""

There are different types of class based views.  ListView, DetailView, CreateView, UpdateView, DeleteView 
and a few more. For example ListView could be used to list the blog posts. 
Django uses these generic class based views to speed up the development process. 
We will see some examples.

#
#

2. We will rewrite the view based functions to see the difference. First import the ListView

"""
from django.views.generic import ListView
"""

#
#

3. Create a class named PostListView for that inherits from ListView. 

"""
class PostListView(ListView):
    pass
"""

#
#

4. Inside the class create a variable called model. This will tell our ListView what model to query.
In this case it will be the Post model.

"""
class PostListView(ListView):
	model = Post

""" 

We will need to add a little more to this class but for now lets see what happens when we use it.

#
#

5. We need to update urls.py from blog to use the ListView instead of the home function.

--> Open blog -> urls.py

Your file should look like this...

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
"""

6. Update urls.py to the following ...

"""
from django.urls import path
from . import views
from . views import PostListView        #ADDED

urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'), #UPDATED
    path('about/',views.about, name='blog-about'),
]

"""

CODE EXPLANATION...

The line below imports the class PostlistView we created.
"""
from .views import PostListView #Changed here
"""

The line below executes the as_view() on PostlistView
"""
path('', PostListView.as_view(), name='blog-home'), #Changed here
"""

#
#

7. Run the developmet server and go to http://127.0.0.1:8000/ You will see an error.

TemplateDoesNotExist at /blog/

blog/post_list.html

Request Method: 	GET
Request URL: 	http://127.0.0.1:8000/blog/
Django Version: 	6.0.3
Exception Type: 	TemplateDoesNotExist
Exception Value:    blog/post_list.html


It is looking for a template with the following naming convention

<app>/<model>_<viewtype>.html

blog/post_list.html

We could create a template with this naming convention but we can also change which template
we want this view to use. As we already have a template for our home view we will change that.

#
#

8. In blog/views.py
    Inside the class PostListView:

    Add the template_name and the term the 
    template uses to access the Post.objects.all()
    behind-the-scenes.

"""
class PostlistView(ListView):
    model = Post
    template_name = 'blog/home.html'    # ADDED
    context_object_name = 'posts'       # ADDED. term template can use 'posts'
"""
[Rob-]

Save the files, run the development server and go to

http://127.0.0.1:8000/blog. 

The home page should now load showing the blog-posts
with our new Class-based view ('PostListView').

#
#

10. Lets chage the ordering of our Posts. Currently we are showing the oldest first. 
To do this we need to change the order our query is making to the database.

--> Open blog -> views.py

Update the class PostListView to the following...

"""
class PostlistView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts' 
    ordering = ['-date_posted']         #ADDED: order the posts from newest to oldest.
"""

#
#

11. Differences of the function based view and class based view.

In this example we are not really saving any lines of code. 
In the function based view we needed to render a function and explicitly pass in information. 
In the class based view we are simply setting variables.  
"""
# function-based view
def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# class-based view (equivalent)
class PostlistView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
"""
[Rob-]

#
#

12. We will create a new view for an individual Post. We will use the DetailView class inside
blog -> views.py

--> Import the DetailView

"""
from django.views.generic import ListView, DetailView
"""

--> Add the following class

"""
class PostDetailView(DetailView):
    model = Post  
"""

#
#

13. Update the url patterns
Open blog -> urls.py

--> Import the PostDetailView
"""
from . views import PostListView, PostDetailView        #UPDATED
"""

At this point we need to create a route that will bring us to a particular Post. To do this 
we will create a url pattern that contains a variable. Each blog post contains an id and we
can create a route that includes variable for an id.

Add the following to your urlpatterns

"""
path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),

"""

The variable <int:pk> pk is what the DetailView expects to be passed. We can also specify the type.
In this case it is an int.

Your full urls.py file should now look like this...

"""
from django.urls import path
from . import views
from . views import PostListView, PostDetailView        #UPDATED


urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'), #UPDATED
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
]

"""

#
#

14. Create a template to display the post details.

The default template name for the class based view is
<app>/<model>_<viewtype>.html
blog/post_detail.html

Let's create one with this format so we do not need to specify a template_name 
as we did in the PostListView(ListView) class.

--> Open blog -> templates -> blog
--> Create a new file named post_detail.html

To get started copy the code from home.html and paste it into post_detail.html

--> Remove the loop {% for post in posts %} {% endfor %}
--> Change all instances of post to object. We do this because the generic DetailView expects object

Should now look like this:
file: blog/post_detail.html

## See changes 'object.' now used instead of 'post.' below...
##          for post in posts: removed
#

{% extends 'blog/base.html' %}
{% block content %}

        <article class="media content-section">
            <div class="media-body">
              <div class="article-metadata">

                <img class="rounded-circle article-img" src="{{ object.author.profile.image.url }}">

                <a class="mr-2" href="#">{{ object.author }}</a>
                <small class="text-muted">{{ object.date_posted |date:'dS, F, Y' }}</small>
              </div>
              <h2><a class="article-title" href="#">{{ object.title }}</a></h2>
              <p class="article-content">{{ object.content }}</p>
            </div>
          </article>
    
{% endblock %}


#
#

15. Run the development server and test a specific post.

--> Go to http://127.0.0.1:8000/blog/post/1
Here you will see your first post.

Try some more examples e.g 

--> Go to http://127.0.0.1:8000/blog/post/1
--> Go to http://127.0.0.1:8000/blog/post/2
--> Go to http://127.0.0.1:8000/blog/post/3


Now try to go to a post with an ID that does not exist.

http://127.0.0.1:8000/blog/post/100

#
#

16. Let's add links that will go to individual posts from our homepage.
At the moment they are dummy links.

e.g.

http://127.0.0.1:8000/#


Open: blog/home.html


    <h2><a class="article-title" href="#">{{ post.title }}</a></h2>


-->Update to:


    <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>


{% url 'post-detail' post.id %}. 

This will look for the post-detail view and pass in the post.id
which is the primary key.


Save all files and re-visit 

/blog

and click on any blog to go to the detail view

NOTICE: the url-ending change: 
e.g.
        .../blog/post/1/

"""
