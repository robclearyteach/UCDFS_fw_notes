"""
Previously we used:
"""
from django.views.generic import ListView, DetailView

"""
Both Django's ListView and DetailView 
allowed us to easily see a list of BlogPosts or 
see the detail of one specific BlogPost.
 
We will now experiment with CreateView to allow
users to add new BlogPosts from the Blog site.

#
#

17. Open blog -> views.py

--> Add an import for CreateView

"""
from django.shortcuts import render
from django.http import HttpResponse
from . models import Post
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView                          #ADDED
)
#[Note: 'import ( )' with round-brackets allows a long line of imports
#        to be listed separately on their own line.]

"""


18. Write a PostCreateView class in views.py

"""
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']  

"""

At this point views.py should look like the following...
"""
from django.shortcuts import render
from django.http import HttpResponse
from . models import Post
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView                          #ADDED
)
#[Note: if you have a long line of imports you can add ( ) to move each to a new line]

class PostCreateView(CreateView):       # NEW
    model = Post
    fields = ['title', 'content']  


class PostDetailView(DetailView):       # FROM BEFORE
    model = Post  
    
    
class PostListView(ListView):           # FROM BEFORE
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'       
    ordering = ['-date_posted']         


#   Older function based views below 

def home(request):                  # NOT USED: PostListView above replaced this
    context_dict={
        'posts': Post.objects.all(),
        'title': 'rob-title'
    }
    return render(request, 'blog/home.html', context_dict)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

"""

#
#

19. Open blog -> urls.py

--> import PostCreateView class
--> Specify urlpattern for PostCreateView

i.e: blog/urls.py should look like the following...
"""
from django.urls import path
from . import views
from . views import (
        PostListView, 
        PostDetailView,
        PostCreateView                                                  # ADDED
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),     
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),    # ADDED: .../blog/post/new
]

"""

#
#

20. 
Create a template called 'post_form.html'. 
(Django defaults to the name "<model>_form.html" as the template for a CreateView.)

As a starting point for post_form.html copy the code from 
    users/register.html

Update post_form.html to contain the following...


{% extends "blog/base.html" %}
{% load crispy_forms_tags %} 
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Blog Post</legend>   
                
                {{ form|crispy }} 
                
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Post</button> 
            </div>
        </form>
        
        {# <!-- Changed here, 'Sign up' div removed --> #}
    </div>
{% endblock content %}
 



#
#

21. Go to http://127.0.0.1:8000/blog/post/new/ 

You will see a form now. 

# Right-click on the page and 'View Page Source'
# Notice: the PostCreateView adds 'Title*' and 'Content*' fields
            with appropriate <input> and <textarea> elements



This again is another example of the power of class based views. 

If you try to fill out the form with something like:

Title: 'Test new'
Content: 'Test new Content'

and Submit ('Post') the form,

You will get the following error 

IntegrityError at /post/new/ 
NOT NULL constraint failed: blog_post.author_id


We are trying to create a post but our author is null which is not allowed. 
If you view the migrations/001_initial.py: we can see why:

"""
...
migrations.CreateModel(
    name='Post',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('title', models.CharField(max_length=100)),
        ('content', models.TextField()),
        ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
        ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),

"""
The 'date_posted' has a default set but every post needs to have an author
and we want the author of the post to be that of the User who is 
currently logged in. 

We can do this by overriding the form_valid() method
in the PostCreateView class of blog/views.py

#
#

22. Open blog -> views.py

--> Update class PostCreateView(CreateView) to the following

"""
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
     
    #Override form_valid() method 
    def form_valid(self, form):
        form.instance.author = self.request.user    # Set the author on the form
        return super().form_valid(form)             # Validate form by running form_valid method from parent class.
"""

This ensures that the submitting “Post” on post_form.html 
 - creates a new post object, 
 - sets its author to the currently logged-in User via the newly added form_valid(), and
 - saves it to the database.
 
 
#
#

23. Run the development server 
--> Go to http://127.0.0.1:8000/post/new/

Try to fill out the form again with something like...
Title: 'Test new 2'
Content: 'Test new Content 2'

and Submit ('Post') the form,

Notice the:

Exception Value: 	
No URL to redirect to. Either provide a url or define a get_absolute_url method on the Model.

What this is telling us is the Post has been created successfully but it does not know where 
to be redirected after the new Post is created.

We can actually see the new Post was created by going to 
    - the homepage http://127.0.0.1:8000/blog 
    OR
    - the DB 'blog_post' table  ('SELECT * FROM blog_post;')

#
#

24. We need to let the view know where we want to redirect. 
[Rob-]
--> Open blog -> models.py

In CreateView, Django does a default call to the Model's:

    'get_absolute_url()' 
    
function and redirects to the URL it returns.
(If this isn't defined, it requires a 'success_url'
to be defined: 
e.g. 
it's as if Django's internal code is something like: 

if self.success_url:
    return redirect(self.success_url)
else:
    return redirect(self.object.get_absolute_url())
)



As we are going to use Django's urls.reverse() to generate the
redirect URL let's import that first...
""" 
from django.urls import reverse      # ADD

"""

Then: update models.py adding a def for 'get_absolute_url()' 

"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse                                 # ADD

# Create your models here.
class Post(models.Model): 
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):                                 # ADDED
        return reverse('post-detail', kwargs={'pk': self.pk})   # redirect to the post-detail view
                                                                #   using the new Post's pk ("primary-key")

"""

    return reverse('post-detail', ...) 

finds the URL pattern named post-detail 
i.e. from blog/urls.py 
...
    # SEE name = 'post-detail' below
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  
      
and inserts self.pk as the post's primary key to generate a URL like
'/post/<pk>' (or more fully: /blog/post/<pk> from mysite/urls.py). 

[The <pk> will be the auto-generated 'id' we saw in migrations/0001_initial.py ]


Django internally does a redirect to the /blog/post/<pk> URL that moves
to the detail-view of that newly created post. 

 ==========
 Try it out: save all changed files and:
 
 --> Go again to http://127.0.0.1:8000/post/new/

Fill out the form again with something like...
Title: 'Test new 3'
Content: 'Test new Content 3'

and Submit ('Post') the form,


See you are now redirected to the detail-view of your new post
See the server log (something like...)

"GET  /blog/post/new/ HTTP/1.1" 200 4378 
"POST /blog/post/new/ HTTP/1.1" 302 0 
"GET  /blog/post/5/   HTTP/1.1" 200 3724


[Rob-]
#
#






25. 
There's a flaw: currently, we can logout and manually visit
our 'New Post' route without a user being logged-in:

/blog/post/new

filling form data and clicking Submit ('Post')
causes an error...

''' 
Exception Type: 	ValueError
Exception Value: 	
Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x0000017FBC0365D0>>": 
    "Post.author" must be a "User" instance.
''' 

We should not be able to create a Post unless we are logged in
(as above: what would the Post.author be?). 


Previously: in users/views.py we added a decorator to the profile() 
view function...

@login_required             # Added decorator here
def profile(request):
    #...


When using Class-based views we inherit from 

django.contrib.auth.mixins.LoginRequiredMixin  

--> Open blog -> views.py and import it.

"""
from django.contrib.auth.mixins import LoginRequiredMixin
"""

--> Update the PostCreateView Class to inherit from LoginRequiredMixin 
    as well as CreateView

"""
class PostCreateView(LoginRequiredMixin, CreateView):
"""

with this in place: try to visit
/blog/post/new

when logged-out (no user logged-in) ...

See that Django generates the URL:

http://127.0.0.1:8000/login/?next=/blog/post/new/

meaning that we need to log-in first before we can 'next' go to /blog/post/new

Your blog/views.py should look something like this now...

"""
from django.shortcuts import render
from django.http import HttpResponse
from . models import Post
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView                          
)
from django.contrib.auth.mixins import LoginRequiredMixin    # ADDED import


class PostCreateView(LoginRequiredMixin,CreateView):        # ADDED LoginRequiredMixin
    model = Post
    fields = ['title', 'content']  
    #Override form_valid() method 
    def form_valid(self, form):
        form.instance.author = self.request.user    
        return super().form_valid(form)             


class PostDetailView(DetailView):
    model = Post  
    
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'       
    ordering = ['-date_posted']         


#   Older function based views below 

def home(request):                  # NOT USED: PostListView above replaced this
    context_dict={
        'posts': Post.objects.all(),
        'title': 'rob-title'
    }
    return render(request, 'blog/home.html', context_dict)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})"""


#
#

26. Next lets add an Update view so users can make changes to posts.
    
    -->  Update blog -> views.py
    
    See the changes below...
"""
[Rob-]
#...
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView                  # ADDED                          
)
#...
# ADD a class-based view for update 
class PostUpdateView(LoginRequiredMixin, UpdateView):       # Inherits from UpdateView & requires login.
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
         
#...
"""

#
#

27. Update blog -> urls.py to the following...
"""
#...
from . views import (
        PostListView, 
        PostDetailView,
        PostCreateView,
        PostUpdateView              # ADDED
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), 
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),            
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),        # ADDED
]

"""
[Rob-]
#
#

28. Test the changes.

--> Run the development server.
--> Login as a current user
--> Visit: http://127.0.0.1:8000/blog/
--> Select any blog Post and click on it
    --> For example clicking on a post might go to URL for post '5'
        http://127.0.0.1:8000/blog/post/5

--> Manually add '.../update' to the URL to go to the new UpdateView:
        http://127.0.0.1:8000/blog/post/5/update/
        
[Notice that form you now see is the same form as for the CreateView.]
Django refers an UpdateView to the same default template name: i.e.: 
    "<model>_form.html"
    
(or in this case: post_form.html).

We created this for the CreateView and so so Django automatically
reuses it for an UpdateView, pre-populating the form 
with the existing post data.


29.

--> Update the blog post and save it by selecting the button named 'Post'
--> The blog post will now show the update information. 
--> Check the blog post on the homepage and you will see the changes 

    http://127.0.0.1:8000/blog/

#
#

30. Currently, login is required to create or update a post.

However, there's a flaw: any logged-in user can visit /update for another user's post,
and edit it...

i.e. try it: 

    from the .../blog/ choose a post from another author (User)
    --> select (click) it to go to the detail view: e.g. you see URL something like...
            http://127.0.0.1:8000/blog/post/5
    
    --> manually add .../update to the end:
            http://127.0.0.1:8000/blog/post/5/update/

    --> change the title/content and click Submit ('Post')
    --> re-vist /blog ('Home')
    --> you should see that you were able to update someone elses Post 
    
    --> In fact the ownership of the post also changes to you after the update!


#
#

[Rob]
31. Let's correct this:

Open blog -> views.py 

Django provides a 'UserPassesTestMixin' class - for use with class-based views. 

If our view inherits from it we can add a 'test_func()' that returns True or False.
If the test_func() returns True: the user can visit the view, otherwise access is denied.  

Otherwise, they are redirected to the login page (if not logged in) 
or shown a 403 Forbidden error (if logged in but not the owner).



--> Update views.py to the following. 

"""
#...
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin      # ADDED

#...
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):          # UPDATED: Inherits above now.
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #Added 'test_func':  check the request to .../update is from the post.author 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
         
"""

--> Test it out...

    --> choose a post from another author (User)
    --> select (click) it to go to the detail view: e.g. you see URL something like...
            http://127.0.0.1:8000/blog/post/4
    
    --> manually add .../update to the end:
            http://127.0.0.1:8000/blog/post/4/update/


    --> you should see a 403 Forbidden error page now!




====
[Rob-]
UserPassesTestMixin.test_func() override:


Code explained...
""" 
def test_func(self):
    post = self.get_object()          # Get the post being accessed
    if self.request.user == post.author:  # Check if current user is the author
        return True                   # Allow access
    return False                      # Deny access

"""    
The test_func() method is meant to return True if the current user passes the test, and False otherwise.

--> post = self.get_object()    
    - fetches the object that the view has been selected for. 
    - get_object() is part of Django's generic detail/update class-based views and 
        returns the object (here, the post) that was selected.

--> if self.request.user == post.author 
    - checks if the current user (the user making the request) is the author of the post. 

#
#

[Rob-]


31. 
Next, let's create a DeleteView.

for blog -> views.py and show the changes in the code with comments.

"""
#...
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView                  # ADDED
)
#...
# ADD a class-based view for delete...
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): 
    model = Post
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
  
"""
[Rob]
The above definition states: 

 To to access this view (Delete)
 
 - user must be logged in, and 
 - the user must be the person who created

#
#

32. As before we must update the url patterns in 
    --> blog/urls.py. 

"""
from django.urls import path
from .views import (
    PostlistView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView                  # ADDED
)
from .import views

urlpatterns = [
    path('', PostlistView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),    # ADDED
    path('about/',views.about, name='blog-about'),
]

"""

#
#

33. Unlike previously, a DeleteView needs a template named 
    'post_confirm_delete.html'.
    
    We will create this inside: blog/templates/blog

    See starter code below...



{% extends "blog/base.html" %}
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Delete Post</legend>
                <h2>Are you sure you want to delete the post "{{ object.title}}"</h2>
            </fieldset>
            <div class="form-group">
                <button class="btn btn-danger" type="submit">Delete</button>
                <a class="btn btn-outline-secondary ms-2" href="{% url 'post-detail' object.id %}">Cancel</a>            
            </div>  
        </form>
    </div>
{% endblock content %}


====
[Rob]
Test it out...

[Happy Path...]

 --> create a new test-delete post (to test the DeleteView on)
    - visit: 
        .../blog/post/new 
    - enter something like...
        title: a post to delete
        conent: delete me soon
    - Submit ('Post') and visit 'Home' (.../blog/)
    
 --> select the newly-added Post
    - notice the url shows something like...
        ...//blog/post/10/

 --> manually add the .../delete to the URL ending 
        .../blog/post/10/delete
        
 --> see the Delete form
 
 --> Choose the 'Cancel' option: 
    - URL moves to 'detail-view' 
        .../blog/post/10/
 
 --> manually add the .../delete again, but 
      choose Delete this time...
      
    
Produces...  
ERROR:
Exception Type: 	ImproperlyConfigured
Exception Value: 	
    No URL to redirect to. Provide a success_url.
    
    

Recall that we have seen a similar error to this before...
    - after submitting a new Post (PostCreateView)
    

This time Django is telling us we need to provide a 
    success_url...

For a DeleteView the post will not be deleted without this.
    

#
#

34. Add a success_url to our PostDeleteView class


--> Open blog -> views.py

Update the class to add the following

"""
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog"               # ADD a redirect back to the 'Home' view after successfully deleting a Post
    
#...

"""
===
Re-test: 
--> go back to see the DeleteView for the Post
        [note: use a number appropriate for your own data ('10' used below.]
        .../blog/post/10/delete
        
 --> choose Delete this time and see the post is deleted...
===




#
#

35. 
We now have CRUD functionality (Create Read Update Delete) 
that is working but we don't have the links in place to 
get to the routes we have created.


Add a link to create a new post.

--> Open blog -> templates -> blog -> base.html

We want to add a link to create a new post when a user is logged in. 
We will add it to the NavBar on the right hand side

"""
        {# <!-- Navbar Right Side --> #}
        <div class="navbar-nav" style="--bs-nav-link-padding-y: 0;">
            {% if user.is_authenticated %}
                {# <!-- ADD a 'New Post' link --> #}
                <a class="nav-item nav-link" href="{% url 'post-create' %}">New Post</a> 
                
                {# ... other links #}

            {% else %}
                <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
            {% endif %}
"""

Note: we've added the link below the 
            {% if user.is_authenticated %}

so that you can only add new posts after you've logged-in. 
Recall this is necessary so there will be an 'author' when the 
PostCreateView.form_valid() runs...
e.g.
        form.instance.author = self.request.user    

#
#

36. Add links to Update and Delete a Post. 

--> Open blog -> templates -> blog -> post_detail.html

"""
{% extends "blog/base.html" %}
{% block content %}
<article class="media content-section">
    <img class="rounded-circle article-img" src="{{ object.author.profile.image.url }}"> 
    <div class="media-body"> 
      <div class="article-metadata">
        <a class="mr-2" href="#">{{ object.author }}</a>
        <small class="text-muted">{{ object.date_posted|date:'dS, F, Y' }}</small>
        
        {# <!-- ADDED: if-block with two links --> #}
        {% if object.author == user %}
          <div>
            <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url 'post-update' object.id %}">Update</a> 
            <a class="btn btn-danger btn-sm mt-1 mb-1" href="{% url 'post-delete' object.id %}">Delete</a> 
          </div>
        {% endif %}
        
      </div>
      <h2 class="article-title">{{ object.title }}</h2>
      <p class="article-content">{{ object.content }}</p>
    </div>
  </article>
{% endblock content %}  

"""

We now have CRUD functionality and links to visit the routes
positioned at appropriate places in the Blog site.

Login with different users and experiment with the 
CRUD links 
    - try to manually add .../update or .../delete
        to user-posts that don't belong to the
        currently logged-in User 
    - try to view Posts for your currently logged-in User 
        & for other users


Also: see if you can find any problems 
(Django Exceptions Page display issues). 

(Note: you may need to login as 'admin'
        & visit the /admin Django Admin page 
        if you get errors with certain users.)

"""