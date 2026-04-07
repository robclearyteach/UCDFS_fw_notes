"""
Unit 3 Walk through Part 2
Django Styling and Navigation 

#
#

1. Update the div of base.html. Make sure to remove the div class container of the original.

Old HTML...

<body>
    <div class = "container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
</body>



#
# 
New HTML... 
file: base.html
<body>
    <main role="main" class="container">
        <div class="row">
            <div class="col-md-8">
            
                {% block content %}{% endblock %}
                
            </div>
            <div class="col-md-4">
                <div class="content-section">
                    <h3>Our Sidebar</h3>
                    <p class='text-muted'>You can put any information here you'd like.</p>
                    <ul class="list-group">
                        <li class="list-group-item list-group-item-light">Latest Posts</li>
                        <li class="list-group-item list-group-item-light">Announcements</li>
                        <li class="list-group-item list-group-item-light">Calendars</li>
                        <li class="list-group-item list-group-item-light">etc</li>
                    </ul>   
                </div>
            </div>
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
</body>


[Rob]
1.1 Save files and re-visit 'blog/' to see the effect.

#
#

2. We will also use some custom css. This will be stored inside the blog app. Create
the following folders static -> blog. Inside the blog directory create a file named main.css.
Your project directory should look like the following.

├── blog
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── migrations
│ │   ├── __init__.py
│ ├── static
│ │   └── blog
│ │       └── main.css
│ ├── templates
│ │   └── blog
│ │       ├── about.html
│ │       ├── base.html
│ │       └── home.html
│ ├── tests.py
│ ├── urls.py
│ ├── views.py

#
#

3.Inside main.css copy and paste the following code

body {
  background: #fafafa;
  color: #333333;
  margin-top: 5rem;
}

h1, h2, h3, h4, h5, h6 {
  color: #444444;
}

ul {
  margin: 0;
}

.bg-steel {
  background-color: #5f788a;
}

.site-header .navbar-nav .nav-link {
  color: #cbd5db;
}

.site-header .navbar-nav .nav-link:hover {
  color: #ffffff;
}

.site-header .navbar-nav .nav-link.active {
  font-weight: 500;
}

.content-section {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-bottom: 20px;
}

.article-title {
  color: #444444;
}

a.article-title:hover {
  color: #428bca;
  text-decoration: none;
}

.article-content {
  white-space: pre-line;
}

.article-img {
  height: 65px;
  width: 65px;
  margin-right: 16px;
}

.article-metadata {
  padding-bottom: 1px;
  margin-bottom: 4px;
  border-bottom: 1px solid #e3e3e3
}

.article-metadata a:hover {
  color: #333;
  text-decoration: none;
}

.article-svg {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}

.account-img {
  height: 125px;
  width: 125px;
  margin-right: 20px;
  margin-bottom: 16px;
}

.account-heading {
  font-size: 2.5rem;
}

#
#

4. We need to link our main.css file to our base html file and load the static files with the following 
code block.

{% load static %}

Place the {% load static %} at the very top of base.html

#
#

5. Add 
    <link rel="stylesheet" type="text/css" href="{% static 'blog/main.css' %}"> 

to base.html.
This creates an absolute path to main.css. 


[Rob]
5.1 Save all changed files and re-visit 'blog/' 
    to see the effect.
    
    [Note: update to: 
      body{ 
            background: red;
        }
    
     #or other striking color if needed
    ]



#
#

6. In base.html
# [Rob]
    Add the following <header> inside the <body> tag
    
    [Note the two <a> links with href="{%% url 'blog-xxxx'}"
    
        The 'blog-xxxx' is the path 'name' in blog.urls
    ]

<header class="site-header">
      <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
        <div class="container">
          <a class="navbar-brand mr-4" href="{% url 'blog-home' %}">Django Blog</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="{% url 'blog-home' %}">Home</a>
              <a class="nav-item nav-link" href="{% url 'blog-about' %}">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              <a class="nav-item nav-link" href="#">Login</a>
              <a class="nav-item nav-link" href="#">Register</a>
            </div>
          </div>
        </div>
      </nav>
    </header>



[Rob]
6.1 Save all changed files and re-visit 'blog/' 
    to see the effect.
#
#




7. The file: 'base.html' will now have the following code.

{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width= , initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">

    <link href="{% static 'blog/main.css' %}" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{% static 'blog/main.css' %}"> 

    {% if title %}
        <title> Django Blog - {{ title }}</title>
    {% else %}
        <title>Django Blog</title>
    {% endif %}
    
</head>

<body>
    <header class="site-header">
      <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
        <div class="container">
          <a class="navbar-brand mr-4" href="{% url 'blog-home' %}">Django Blog</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="{% url 'blog-home' %}">Home</a>
              <a class="nav-item nav-link" href="{% url 'blog-about' %}">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              <a class="nav-item nav-link" href="#">Login</a>
              <a class="nav-item nav-link" href="#">Register</a>
            </div>
          </div>
        </div>
      </nav>
    </header>
    <main role="main" class="container">
        <div class="row">
            <div class="col-md-8">
            
                {% block content %}{% endblock %}
                
            </div>
            <div class="col-md-4">
                <div class="content-section">
                    <h3>Our Sidebar</h3>
                    <p class='text-muted'>You can put any information here you'd like.
                    <ul class="list-group">
                        <li class="list-group-item list-group-item-light">Latest Posts</li>
                        <li class="list-group-item list-group-item-light">Announcements</li>
                        <li class="list-group-item list-group-item-light">Calendars</li>
                        <li class="list-group-item list-group-item-light">etc</li>
                    </ul>
                    </p>
                </div>
            </div>
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
</body>

</html>
#
#






8. Possible Issue:
In the above: when revisiting 'blog/' to see the changes in styling taking place.
    You may beed to refresh your browser, the server or clear the cache.

#
#

9. Possible Issue:
    Error: during template rendering. You may encounter the following error.
NoReverseMatch at /
Reverse for 'blog-home' not found. 'blog-home' is not a valid view function or pattern name.

If this occurs check your blog -> urls.py file to see if 'blog-home' is a valid view function or pattern name.
If not make the changes and retest.


#
#

10. Update home.html 

From ... 

{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
        <h1>{{ post.title }}</h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock content %} 

To ...  

{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
            <div class="media-body">
              <div class="article-metadata">
                <a class="mr-2" href="#">{{ post.author }}</a>
                <small class="text-muted">{{ post.date_posted }}</small>
              </div>
              <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
              <p class="article-content">{{ post.content }}</p>
            </div>
          </article>
    {% endfor %}
{% endblock content %}    


The update includes class for styling each blog post. 

#
#

11. At this point all links bar Login and Register should be working.

  
"""







