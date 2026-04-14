#TASK: 20 - 40min 
 # Using sharedfolder djangotutorial_task/
 
 # Repeat the updates made from the previous session (4).
 # See if you can make the changes alone:
 #	[Note: see djangotutorial/ if stuck]
 #
 # TASK BREAKDOWN
 
#	* add 
#	|- polls/templates/polls/
#		- base.html					#boilerplate with template-tag for content
#		- index.html 				# extends with <h3> ul>li*3
#
#
#	* Copy-paste the Models code from the Django tutorial:
#		- https://docs.djangoproject.com/en/6.0/intro/tutorial02/#id2

#	* Make migrations

#	* migrate

#	* switch to shell

#	* import models and create a question with some choices
#	* save it to the db
#	* run a few ORM API calls 
#			(try from memory, look back if needed)

#	* Alter polls/models.py to access the DB 
#		with the ORM API and send DB data to 
#		the 'home.html'template

#	* write the template code to:
#		for each question in questions:
#		<h3> question text </h3>
#			<ul>
#			for each choice in the choice_set:
# 				<li> choice text and vote count </li>
#		
