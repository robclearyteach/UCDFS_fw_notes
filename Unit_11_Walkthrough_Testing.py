"""
Unit 11 Walk through 

Testing

Here we will learn how to perform testing in Django and learn the power of 
automated testing. We will build tests in both the Blog and Users apps.

- RUNNING TESTS FROM CLI

**To run all tests in both apps we use**
    python manage.py test

**To run all tests in a specific app we use**
python manage.py test (name_of_app)

    python manage.py test blog
    python manage.py test users

**To run all tests in a specific class in a test file we use**
python manage.py test blog.tests.classname

    python manage.py test blog.tests.PostModelTests
    python manage.py test blog.tests.PostViewsTests

**To run a single test in a specific class in a test file we use**
python manage.py test blog.tests.classname.test_method

    python manage.py test blog.tests.PostModelTests.test_post_content
    python manage.py test blog.tests.PostViewsTests.test_post_list_view
# 
# 

## =======================================
#       Testing the 'blog' app 
## =======================================
"""
# blog/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from . models import Post

"""

These lines import necessary classes and functions.

TestCase    - from Django's test framework - can be used to create our test cases.
Client      - from Django's test framework - acts as a dummy web browser for simulating GET and POST requests on a URL.
User        - Django's default user model.
reverse     - the Django function that generates a URL from it's site-wide name.
Post        - the model class we are going to test.


#
#
Write a Test class
"""
class PostTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.post = Post.objects.create(
            author=cls.user, 
            title='Test Post', 
            content='This is a test post'
        )
        
    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{post.author}'
        expected_title = f'{post.title}'
        expected_content = f'{post.content}'
        self.assertEqual(expected_author, 'testuser')
        self.assertEqual(expected_title, 'Test Post')
        self.assertEqual(expected_content, 'This is a test post')
"""

- The Django test framework creates a temporary test-database before tests run 
    and destroys it afterward.
- It begins the TestCase setup by calling setUpTestData()


##
# @ setUpTestData() 
- is called once for the whole TestCase class.
- it creates data shared by all tests.  
- The data it creates and the test methods we define 
    run against this test-database.



##
# @ setUpTestData(cls):    

- User.objects.create_user()    - creates a user in the one-off test database.

- Post.objects.create(..)       - creates a post in the one-off test database:
                                  it associates the post with the user just created
                                  (cls.user).

# 
# 

## =======================================
#       Testing the 'blog' model: Post 
## =======================================

2.  
2.1 Create a test-case 
"""
def test_post_content(self):
    post = Post.objects.get(id=1)
    expected_author = f'{post.author}'
    expected_title = f'{post.title}'
    expected_content = f'{post.content}'
    self.assertEqual(expected_author, 'testuser')
    self.assertEqual(expected_title, 'Test Post')
    self.assertEqual(expected_content, 'This is a test post')
"""

- The intent of this test-case is to test that 
    the content of the Post created in setUpTestData() 
    is as expected:
  
- Post.objects.get(id=1):
    'id=1' will get the single Post record from the test-database.

- It then checks that the 
      author, 
      title, 
      content 
  match what setUpTestData() created.
  
  (Note: this is a simple test to get started.)


2.2: Run the test-case:
$ python manage.py test blog.tests.PostTests

>
    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.466s

    OK
    Destroying test database for alias 'default'...
# 
# 

3.  
3.1 Create another test
"""
def test_post_str_method(self):
    post = Post.objects.get(id=1)
    self.assertEqual(str(post), post.title)
"""

- The intent of this test-case is to check that
    the __str__() method of the Post model
    produces what we expect.

- In this case: the post.title setUpTestData() created:
    'This is a test post'



3.2 Run the test-case:

$ python manage.py test blog.tests.PostTests


>
    Found 2 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .F
    ======================================================================
    FAIL: test_post_str_method (blog.tests.PostTests.test_post_str_method)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "...djangotutorial\blog\tests.py", line 31, in test_post_str_method
        self.assertEqual(str(post), post.title)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: 'Post: Test Post' != 'Test Post'
    - Post: Test Post
    ? ------
    + Test Post


    ----------------------------------------------------------------------
    Ran 2 tests in 0.453s


3.3 Fix the failing test-case:

    - The test-case failed because the current 
        blog/models.py --> Post.__str__() has:
        #...
            return f"{self.__class__.__name__}: {self.title}"

    - our test-case epected just 'self.title'
    
    - So, let's update the models.py code to:
            return f"{self.title}"
        
        and re-run the test-case...
        

$ py manage.py test blog.tests.PostTests

>
    Found 2 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.451s

    OK
    Destroying test database for alias 'default'...


#
# Both test-cases pass this time!
# 


#
#

4.  
As per the above, 
let's continue with further examples...



4.1 Write a test-case for the 
        Post.get_absolute_url() 
    
"""
def test_get_absolute_url(self):
    post = Post.objects.get(id=1)
    self.assertEqual(post.get_absolute_url(), 'blog/post/1')
"""

- The intent of this test-case is to check that
    the Post.get_absolute_url() is returning what is expected:

    See-> blog/models.py
            |-> class Post(models.Model): ...
                #...
                def get_absolute_url(self):                                 
                    return reverse('post-detail', kwargs={'pk': self.pk})   
                                                                    
   
    - for a Post with 'id=1' 
        (the test-database's single Post created by setUpTestData(...) ) 
        
        we might expect the 'post-detail' URL-ending to produce:
            .../blog/post/1
        
    - We can assertEqual() comparing to that literal string 
            'blog/post/1'
     
      in the test-case to test it.

    - This time: let's just run that single test-case to see:
        (See top-of-file examples show how to do this...)
    
$ py manage.py test blog.tests.PostTests.test_get_absolute_url
>
    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F
    ======================================================================
    FAIL: test_get_absolute_url (blog.tests.PostTests.test_get_absolute_url)
    ----------------------------------------------------------------------
    ...
    AssertionError: '/blog/post/1/' != '/blog/post/1'
    - /blog/post/1/
    ?             -
    + /blog/post/1
    ...
    FAILED (failures=1)

   
    - TASK: Examine the test-case output and try to figure-out
            why it failed 
            [Tip: '/']



4.2 Fix the failing test-case:

    - Make a change to the assertEqual() and get the test-case
      to pass.
      
    - We could also use django.urls.reverse()
        in the actual test-case for this...
        
"""
def test_get_absolute_url(self):
    post = Post.objects.get(id=1)
    self.assertEqual(post.get_absolute_url(), reverse('post-detail', args=[post.id]))
"""    

    - [NOTE: in blog/models.py --> Post.get_absolute_url()
                we use django.urls.reverse passing a kwargs={} (dict)
                
                Here we're showing the variant passing args=[]
                that does the same thing in this case.
      ] 

# 
# 


"""

"""
## =======================================
#       Testing the 'blog' Post: views 
## =======================================

5.  
Create a new Test class:
    - blog/tests.py
    - use setUp() (instance-method) this time
        (as opposed to setUpTestData() last time)

"""
class PostViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            author=self.user, 
            title='Test Post', 
            content='This is a test post'
        )
"""

##
# setUp() 

    - Runs before every single test-case method
    - Creates fresh objects each time
        i.e.  above: 
              a new 'Client', 'User' and 'Post' are created 
              for each test-case of the class

    - Use setUp() when...
        
        - test-cases should run with a particular start-state:
            test-database objects have particular values to begin with
        
        - test-cases expected to change the objects 
            (e.g. self.post.title = <new-value>...)

# 
# 

6.  Add TestCases...
"""
def test_post_list_view(self):
    url = reverse('blog-home')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This is a test post')
    self.assertTemplateUsed(response, 'blog/home.html')
"""

- The intent of this test case is to check that 
        - the blog-home view loads correctly returning a successful 200 OK response
        - contains content from an expected post ("This is a test post"), and 
        - renders the correct template (blog/home.html)
        - It the ListView for the /blog (home page).


- It simulates a GET request


$ py manage.py test blog.tests.PostViewTests.test_post_list_view
>
    Found 1 test(s).
    Creating test database for alias 'default'...
    ...
    --------------------------------------------------------------------
    Ran 1 test in 0.474s

    OK
    Destroying test database for alias 'default'...


# 
# 

7.  
"""
def test_post_detail_view(self):
    url = reverse('post-detail', args=[self.post.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.post.title)
"""

- The intent of this test-case is to check that 
        - the post-detail view loads successfully, returns a 200 OK response
        - displays the expected post title for the requested post
        
- [NOTICE: 
    the reverse() uses 
        'self.post.id' 
    
    this time instead of the 
        'Post.objects.get(id=1)' 
    
    previously. 
    This is because the setUp() created and set the 
        'self.post'
    instance variable to our test Post object.]



##
# Let's test just this single test-case...

$ py manage.py test blog.tests.PostViewTests.test_post_detail_view
>
    Found 1 test(s).
    ...
    ----------------------------------------------------------------------
    Ran 1 test in 0.465s

    OK



# 
# 

8.  
"""
def test_create_post_view(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('post-create'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

    response = self.client.post(reverse('post-create'), {
        'title': 'New title',
        'content': 'New text',
    })
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertTrue(Post.objects.filter(title='New title').exists())
"""

- The intent of this test case is to check that 
  the PostCreateView:  
        - is accessible to a logged-in user ('testuser')
        - accepts a GET request to 'post-create' URL-ending (e.g. '/blog/post/new')
        - renders the expected (post_form.html) to the GET request
        - accepts a POST request to 'post-create' URL-ending 
        - allows a Post to be created with 'title' and 'content'
        - redirects after Post-creation 
        - confirms the post exists in the test-database after the POST request.
        

##
# Let's run the test-case...
#

$ py manage.py test blog.tests.PostViewTests.test_create_post_view
>
    Found 1 test(s).
    ...
    Ran 1 test in 0.927s
    ...
    OK
# 
# 

9.  
"""
def test_update_post_view(self):
    self.client.login(username='testuser', password='12345')
    url = reverse('post-update', kwargs={'pk': self.post.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

    response = self.client.post(url, {
        'title': 'Updated title',
        'content': 'Updated text',
    })
    self.post.refresh_from_db()
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertEqual(self.post.title, 'Updated title')
"""

- The intent of this test case is to check that 
  the PostUpdateView:  
        - is accessible to a logged-in user ('testuser')
        - accepts a GET request to 'post-update' URL-ending (e.g. '/blog/1/create')
        - renders the expected (post_form.html) to the GET request
        - accepts a POST request to the URL-ending 
            allowing 'title' and 'content' updates
        - redirects after Post has been updated  
        - confirms the post title is the 'Updated title' after the update.
        
- [NOTE: the test-case uses 
        
        'self.post.refresh_from_db()' 
        
        to reload the object from the database at that point in time.
  ]        
  
# 
# 

10. test_delete_post_view method
"""

def test_delete_post_view(self):
    self.client.login(username='testuser', password='12345')
    url = reverse('post-delete', kwargs={'pk': self.post.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    response = self.client.post(url)
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
"""
- The intent of this test case is to check that 
  the PostUpdateView:  
        - is accessible to a logged-in user ('testuser')
        - accepts a GET request to 'post-delete' URL-ending (e.g. '/blog/1/delete')
        - renders the expected (post_confirm_delete.html) to the GET request
        - accepts a POST request to the URL-ending 
            simulating submiting the form (via 'Delete' button)
        - redirects after Post has been deleted  
        - confirms that after the delete - no post exists with the 'pk' of the original
            i.e. it has been deleted from the test-database. 

# 
# 



"""

"""
## =======================================
#       Testing the 'users' app 
## =======================================

"""
# Open:
#    users/tests.py
#    users/models.py (view class Profile)

"""
import


"""
from django.test import TestCase
from django.contrib.auth.models import User
#new for User Register, Profile and Update
from django.core.files.uploadedfile import SimpleUploadedFile
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from . models import Profile

"""
[Rob-]



#
#
Write a Test class
"""
class UserFormTests(TestCase):

    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.create(user=self.user, image='default.png')
        
        
"""
##
# @ setUp()
    - User.objects.create_user()            - creates a User in the one-off test database.
    - Profile.object.create( :user, :image) - creates a Profile and associates to that User
    
[NOTE: In general: a more robust way to create a profile would be with:
    #get_or_create()
    
    # i.e. ...
        Profile.objects.get_or_create(user=self.user, defaults={'image': 'default.png'}) 
    
    - get_or_create() first checks if a profile for that user already exists. 
        If it does, it returns it; if not, it creates one
        
    - 'defaults' dict can be used to assign values to fields.
        (Typically used for mandatory fields to ensure they have a value)
"""

"""



#
#

12. 
"""
def test_user_register_form(self):
    # Test user registration form with valid data
    form_data = {
        'username': 'newuser', 
        'email': 'newuser@example.com', 
        'password1': 'django1234', 
        'password2': 'django1234'
    }
    form = UserRegisterForm(data=form_data)
    self.assertTrue(form.is_valid())

"""
- The intent of this test-case is to check that
    - the UserRegisterForm accepts valid input-data and passes validation

    - form_data = {...} provides sample form inputs (username, email, matching passwords)
    - form.is_valid() runs the form's validation checks for the fields provided.


[Rob-]

##
# Let's test it...

$ py manage.py test users.tests.UserFormTests.test_user_register_form
>
    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.494s

    OK


[Rob-]
#
#

13. 
"""
def test_user_update_form(self):
    # Test user update form with valid data
    form_data = {
        'username': 'updateduser', 
        'email': 'updateduser@example.com'
    }
    form = UserUpdateForm(data=form_data, instance=self.user)
    self.assertTrue(form.is_valid())
    form.save()
    self.user.refresh_from_db()
    self.assertEqual(self.user.username, 'updateduser')
"""

- the intent of this test-case is to check that 
    - the UserUpdateForm correctly updates a User when given valid update data 

    - form_data = {...} provides sample form inputs (updated_username, updated_email)

    - UserUpdateForm(:data, :instance) - takes the form_data and the self.user created in setUp() 
    
    - save() & refresh_from_db() - write to the test-database and reload the User object 
                after update
                
    - finally the test-case checks if the User's username is the updated one
    
  [Rob-]
  
##
# Let's test it...

$ py manage.py test users.tests.UserFormTests.test_user_update_form
>
    Found 1 test(s).
    ...
    Ran 1 test in 0.483s
    ...
    OK

#
#
14. 
"""
def test_profile_update_with_invalid_image_format(self):
    # Test profile update with an invalid image format
    invalid_image_data = b'this is not real image data'
    invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
    form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
    self.assertFalse(form.is_valid())

"""
- the intent of this test-case is to check that
    - the ProfileUpdateForm rejects invalid image uploads and fails validation

    - invalid_image_data = b'...' simulates corrupted/non-image file content
            the b'...' represents raw binary file data.test_post_str_method
            a real image would contain encoded binary content 
            (e.g., JPEG/PNG byte stream) instead of plain text
            
    - SimpleUploadedFile(...) simulates an uploaded file Object with .txt 
        extension, text/plain content type, and the corruppted data from above.

    - ProfileUpdateForm(files={'image': ...}, instance=self.user.profile) 
      binds the invalid file to the User instance created in setUp()

    - finally the test-case checks that the form is not valid (assertFalse)
    


##
# Let's test it...
  
$ py manage.py test users.tests.UserFormTests.test_profile_update_with_invalid_image_format
>
    Found 1 test(s).
    ...
    OK


#
#

15. test_profile_update_with_oversized_image()
"""
def test_profile_update_with_oversized_image(self):
    # Test profile update with an oversized image
    oversized_image_data = b'\x00' * 5242880  # 5MB of zeros
    oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
    form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
    self.assertFalse(form.is_valid())
"""
- the intent of this test-case is to check that
    - the ProfileUpdateForm rejects image uploads that exceed a certain size limit

    - oversized_image_data = b'\x00' * 5242880 simulates a 5MB binary file 
            (made entirely of all-zero bytes)

    - SimpleUploadedFile(...) creates a fake JPEG file upload with that oversized content

    - ProfileUpdateForm(files={'image': ...}, instance=self.user.profile)
      binds the invalid file to the User instance created in setUp()

    - finally the test-case checks that the form is not valid (assertFalse)
    
[Rob-]

##
# Let's test it...
  
$ py manage.py test users.tests.UserFormTests.test_profile_update_with_oversized_image
>
    Found 1 test(s).
    ...
    OK




#
#
## =======================================
#       Testing with 'coverage'
## =======================================



16. 
- coverage is a Python tool that measures how much of your code is executed when running tests
- it shows which lines of code were run and which were not during testing

-  Installation
"""
pip install coverage

"""

- Basic Usage
To use coverage.py, you typically follow these steps:

Run Your Tests with Coverage


$ coverage run manage.py test
>
    Found 12 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 6.007s

    OK
    Destroying test database for alias 'default'...
"""

"""
- Generate a Report
After running your tests with coverage, you can generate a report


##
# Output to the console

$ coverage report
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
blog\__init__.py                                   0      0   100%
blog\admin.py                                      3      0   100%
blog\apps.py                                       3      0   100%
blog\migrations\0001_initial.py                    8      0   100%
blog\migrations\__init__.py                        0      0   100%
blog\models.py                                    13      0   100%
blog\tests.py                                     66      0   100%
blog\urls.py                                       4      0   100%
...
users\tests.py                                    30      0   100%
users\views.py                                    31     22    29%
------------------------------------------------------------------
TOTAL                                            309     34    89%
"""

"""
##
# Output to HTML
#
Again, *after* running your tests with coverage
you can generate an HTML report

$ coverage html
>
    Wrote HTML report to htmlcov\index.html
    
    
Your djangoproject folder should then have:
djangoproject/
    |- htmlcov/
        |- ...
        |- index.html       #Find this
        
Open index.html, copy-path and open in a browser.
Briefly explore what it provides...


"""
This will create a directory called htmlcov containing an interactive HTML report. 
You can open htmlcov/index.html in your web browser to view it.

"""

** Remember to add lines:

htmlcov/ 
.coverage 

to your .gitignore file, 
    as you typically don't want to include coverage data 
    and HTML reports in your version control system. **
"""


""" 
TASK:
    Visit the Django documentation links introducing Testing below:

[NOTE: for experimenting with testing in Django shell:

@See Error below: 'Invalid HTTP_HOST...'testserver'...
@See fix below

$ py manage.py shell
>>> from django.test.utils import setup_test_environment
>>> from django.test import Client
>>> client = Client()

#
# ERROR 
#
>>> response = client.get("/blog/")
Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
...
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.

#
# FIX
#
>>> from django.test.utils import override_settings
>>> override_settings(ALLOWED_HOSTS=["testserver"]).enable()


#
# should work thereafter...
#
>>> response = client.get("/blog/")
>>> response
<TemplateResponse status_code=200, "text/html; charset=utf-8">
>>> 
>>> response.status_code
200
>>> print(response.content.decode("utf-8"))
...
>>> from blog.models import Post
>>> Post.objects.all()
<QuerySet [<Post: Test BlogPost 1>, <Post: Test BlogPost 2>, <Post: Test BlogPost 3>, <Post: django admin test 1>, <Post: test black panther>, <Post: test new updated>, <Post: updated by blackpanther>]>
...
>>> from django.urls import reverse
>>> url = reverse('post-detail', args=[1])           
>>> url
'/blog/post/1/'
>>> response = client.get(url)
>>> print(response.content.decode("utf-8"))
]
  
  
  
    
    https://docs.djangoproject.com/en/6.0/intro/tutorial05/#the-django-test-client
        
        - recommended: follow the Django Shell experiments
                        except apply to this 'djangoproject' Blog Site 
            
            - alternatively (or combined): if djangotutorial complete:
                        follow the django testing tutorial:
            
            https://docs.djangoproject.com/en/6.0/intro/tutorial05/#writing-our-first-test


    https://docs.djangoproject.com/en/6.0/intro/tutorial05/#introducing-automated-testing
        
        - recommended to read 
"""
""" 
SUMMARY

Importance of Automated Testing

1. Quality Assurance 
   Automated tests help ensure that the code works as expected and that new changes don't break existing functionality. 
   This is crucial for maintaining the integrity of a web application over time.

2. Efficiency 
   Writing tests for Django applications automates the process of checking for errors, saving developers time and effort compared to manual testing. 
   This allows for more frequent testing and faster development cycles.

3. Refactoring Confidence 
   Automated tests provide a safety net that gives developers the confidence to refactor and improve the code without fear of introducing regressions.

4. Documentation 
   Tests can serve as a form of documentation for your code. 
   They provide insights into what the code is supposed to do, which can be helpful for new developers joining a project.

5. Debugging 
   When tests fail, they can pinpoint the exact location of problems, making debugging much easier and faster.

6. Continuous Integration (CI) 
   Automated tests are integral to CI/CD pipelines. 
   When tests are automated, they can be run every time code is pushed to a repository, ensuring that only code that passes all tests is deployed.

7. Scalability 
   As a Django application grows, manual testing becomes less practical. 
   Automated testing scales much more effectively with the size of the project.

8. Risk Mitigation 
   By catching issues early in the development process, automated tests reduce the risk of bugs making it to production, 
   which can be costly to fix and damaging to user trust.

9. Test Coverage 
   Tools can measure test coverage, the proportion of your codebase tested by automated tests, 
   which is a key metric for understanding the effectiveness of your testing strategy.

10. Development Culture 
    Automated testing promotes a culture of quality and accountability. 
    It encourages writing testable code and considering edge cases and potential errors during the development process.

"""


