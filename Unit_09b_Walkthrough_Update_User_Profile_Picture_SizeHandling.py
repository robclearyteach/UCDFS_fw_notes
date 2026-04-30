"""
[Rob]
--> Change the Username
--> Change the Email
--> Select Update and you should see the new changes


[ Note: check the /admin  or the DB
        will confirm no new user has been created, 
        but you will see the updated data in the DB.
]

#
#

17. 
At the moment, when we add the image to the Profile
we're using it's natural resolution (and size) 

--> Right click on the profile image and open in a new tab.
    Hover/view the tab <title>
    e.g.
        'profile_img_blackpanther.png (PNG Image, 4024 × 4220 pixels)'
    
    OR in Console:
        >document.querySelector('img').naturalWidth 
        >document.querySelector('img').naturalHeight

--> USE JS Console to view file-size:
        > src = document.querySelector('img').src
        >fetch(src)
            .then( r=>r.blob() )
            .then( b=> console.log(`img-size: ${ (b.size/1024/1024).toFixed(2) }MB`) )
  
    [Similarly: open the 'Network' tab of the Browser Inspector
                and view the 'size' column]  


Whats happening is our css is scaling this image down for the profile pic but the web application 
is still storing this large file and it needs to send it to the browser every time which can slow down the web app.




18. Use Python pillow to resize the picture before saving.
    [Pillow should already be installed from a previous task:
        if not: install it before you continue:
        pip install pillow
        

--> Open users/models.py 

--> Override the default save() method:
    See code below...

Ensure you import Image from pillow:
"""
from PIL import Image
"""

"""
from django.db import models
from django.contrib.auth.models import User
from PIL import Image                           # NEEDED

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    """
    Changes here explained below
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

"""


CODE EXPLANATION...

-->. Override default save() from models.Model
      & call the default save() behaviour before adding to it. 
"""
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
"""

[Rob-]
The above save() stores the model data in DB, 
    i.e. just the image file path
    (recall that the actual image is saved to disk in MEDIA_ROOT ).
    
[NOTE:
    View the DB 'users_profile' table to better understand this if needed.
]
   

"""
img = Image.open(self.image.path)

"""
→ opens the saved file using Pillow (self.image is the Profile.image 'ImageField' )
"""

if img.height > 300 or img.width > 300:
    """"""
"""
--> checks if the size is above 300 x 300
"""
output_size = (300, 300)
img.thumbnail(output_size)
img.save(self.image.path)
"""
--> shrinks it to max 300×300, then overwrites the file on disk

The thumbnail() method modifies the image in place to fit within the specified dimensions while maintaining the original aspect ratio.
After resizing, the modified image is saved back to its original path, overwriting the original image.

#
#

19. Test the changes

--> Open http://127.0.0.1:8000/profile/
--> Add a new profile pic: re-add the original profile_pic 
--> Submit 'Update'

view MEDIA_ROOT/profile_pics and view the file size

#
#

20. It's worth noting there are many ways to resize an image. At the moment if you look at 
media/profile_pics you will see all the images are still stored. You could add the functionality that 
for every new picture added an old one is deleted but for now we won't concern ourselves
with that functionality.
#
#

[Rob-]

#
#
21.
Next: if we navigate to 'Home' we'll see that the Blog posts
currently don't display a profile_pic for each 'post'


22. Display the image of the author beside each post on the home page.

--> Open blog/app/templates/home.html

--> Add the following line to home.html

<img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}">


BELOW: Full code for updated home.html:
"""
"""

{% extends "blog/base.html" %}
{% block content %}

    {% for post in posts %}
        <article class="media content-section">
            <div class="media-body">
              <div class="article-metadata">
                {# <!-- ADDED <img> --> #}
                <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}">

                <a class="mr-2" href="#">{{ post.author }}</a>
                <small class="text-muted">{{ post.date_posted |date:'dS, F, Y' }}</small>
              </div>
              <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
              <p class="article-content">{{ post.content }}</p>
            </div>
          </article>
    {% endfor %}
    
{% endblock content %}    

"""
"""


Save all files 
Refresh the browser
Visit 'Home' (/blog)

[NOTE: if you don't see profile_pics attached to posts
        consider why?
        
        Try adding 
            <div>{{ post.author }}</div>
            <div>{{ post.author.profile }}</div>

        Then Try: 
            Visit /admin 
            Add a post for a user with a profile and save
            re-visit 'Home' /blog
]

[NOTE: if getting problems with the default.jpg image
        download this :
        
            https://commons.wikimedia.org/wiki/File:Default_pfp.jpg
            
        save and overwrite the current 'default.jpg'
]
"""


