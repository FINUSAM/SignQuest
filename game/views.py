import json
import random
from django.apps import apps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

MalayalamAlphabetModel = apps.get_model('home', 'MalayalamAlphabetModel')
previous_selected_question = None

# Create your views here.

@login_required
def game(request):
    games = ['flashcard', 'ordering', 'quiz']
    return render(request, 'game/game.html', {'games':games})

@login_required
def flashcard_levels(request):
    no_of_levels = 4
    return render(request, 'game/flashcard_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def flashcard(request, level):
    all_alphabets = MalayalamAlphabetModel.objects.all()
    alphabet_list = {}
    for alphabet in all_alphabets:
        alphabet_list[alphabet.mal] = alphabet.image.url
    return render(request, 'game/flashcard.html', {'level':level+1, 'alphabet_list':alphabet_list})

@login_required
def ordering_levels(request):
    no_of_levels = 2
    return render(request, 'game/ordering_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def ordering_alphabet(request):
    all_alphabets = MalayalamAlphabetModel.objects.all()
    alphabet_list = []
    for alphabet in all_alphabets:
        alphabet_list.append(alphabet.mal)
    return render(request, 'game/ordering alphabet.html', {'alphabet_list':alphabet_list})

@login_required
def ordering_image(request):
    all_alphabets = MalayalamAlphabetModel.objects.all()
    alphabet_list = []
    for alphabet in all_alphabets:
        alphabet_list.append(alphabet.image.url)
    return render(request, 'game/ordering_image.html', {'alphabet_list':alphabet_list})

@login_required
def quiz_levels(request):
    no_of_levels = 3
    return render(request, 'game/quiz_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def quiz_normal(request, level):
    if request.method == 'POST':
        selected_answer = request.POST.get('selected-answer')
        correct_answer = previous_selected_question.eng
        
        if selected_answer == correct_answer:
            result = "CORRECT"
        else:
            result = "WRONG"

        messages.success(request, result)
        return redirect('quiz_normal', level)
    
    
    all_alphabets = MalayalamAlphabetModel.objects.all()
    current_selected_question = selectRandomQuestion(all_alphabets)
    selected_options = getRandomOptions(all_alphabets, current_selected_question)

    if level == 2:
        data = {
            'question': current_selected_question.mal,
            'options':[{'eng':option.eng, 'image':option.image.url} for option in selected_options]
        }
    elif level == 1:
        data = {
            'question': current_selected_question.image.url,
            'options':[{'eng':option.eng, 'mal':option.mal} for option in selected_options]
        }
    else:
        redirect('quiz_levels')


    return render(request, 'game/quiz_normal.html', data)

def quiz_ai(request):
    return redirect('quiz_levels')

def selectRandomQuestion(all_alphabets):
    global previous_selected_question
    while True:
        new_selected_question = random.choices(all_alphabets)[0]
        if new_selected_question != previous_selected_question:
            break
    previous_selected_question = new_selected_question
    return new_selected_question

def getRandomOptions(all_alphabets, current_selected_question):
    modified_all_questions = [question for question in all_alphabets if question != current_selected_question]
    selected_options = random.sample(modified_all_questions, 3)
    selected_options.append(current_selected_question)
    random.shuffle(selected_options)
    return selected_options
