from django.shortcuts import render
from . models import Question

def index(request):
    db_questions = Question.objects.all()
    
    return render(request, 'polls/index.html', {'questions':db_questions})