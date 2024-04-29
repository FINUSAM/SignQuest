from datetime import datetime
from django.http import HttpResponse
import random
from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib import messages

UserStatsModel = apps.get_model('account', 'UserStatsModel')
MalayalamAlphabetModel = apps.get_model('home', 'MalayalamAlphabetModel')

previous_selected_question = None
previous_submission_time = None

# Create your views here.

def learning(request):
    all_alphabets = MalayalamAlphabetModel.objects.all()
    alphabets_eng = [alphabet.eng for alphabet in all_alphabets]
    
    if request.method == 'POST':
        time_taken = datetime.now() - previous_submission_time
        selected_answer = request.POST.get('selected-answer')
        is_answer_shown = request.POST.get('is-answer-shown')
        correct_answer = previous_selected_question.eng
        result = change_confidence_level(request.user, correct_answer, selected_answer, alphabets_eng, time_taken, is_answer_shown)
        messages.success(request, result)
        return redirect('learning')
    
    weights = get_user_confidence_level(all_alphabets, request.user)
    current_selected_question = selectRandomQuestion(all_alphabets, weights)
    selected_options = getRandomOptions(all_alphabets, current_selected_question)
    learning_counter = UserStatsModel.objects.get(user=request.user).learning_counter

    confidence_color_levels_and_letters = []
    confidence_color_levels_only = [(1 - x)+0.05 if x != 0 else x+0.05 for x in weights]

    for index,letter in enumerate(alphabets_eng):
        if index>=learning_counter:
            break
        confidence_color_levels_and_letters.append([letter, confidence_color_levels_only[index]])


    data = {
        'question': current_selected_question.image.url,
        'options':[{'eng':option.eng, 'mal':option.mal} for option in selected_options],
        'confidence_color_level': confidence_color_levels_and_letters,#[(1 - x)+0.05 if x != 0 else x+0.05 for x in weights],
    }

    return render(request, 'learning/learning.html', data)

def answer(request):
    try:
        answer = previous_selected_question.mal
    except:
        answer = 'Answer not available. Try Reloading the page'
    return HttpResponse(answer)

##Required Functions

def get_user_confidence_level(all_alphabets, user):
    stats = UserStatsModel.objects.get(user=user)
    confidence_levels = []
    for alphabet in all_alphabets:
        confidence_levels.append(getattr(stats, alphabet.eng))
    #returns [1, 1, 1, 0, 0]
    return confidence_levels
    
def selectRandomQuestion(all_alphabets, weights):
    global previous_submission_time
    global previous_selected_question
    while True:
        new_selected_question = random.choices(all_alphabets, weights)[0]
        if new_selected_question != previous_selected_question:
            break
    previous_selected_question = new_selected_question
    previous_submission_time = datetime.now()

    return new_selected_question

def getRandomOptions(all_alphabets, current_selected_question):
    modified_all_questions = [question for question in all_alphabets if question != current_selected_question]
    selected_options = random.sample(modified_all_questions, 3)
    selected_options.append(current_selected_question)
    random.shuffle(selected_options)
    #selected_options = [option.answer for option in selected_options]
    return selected_options


def change_confidence_level(user, correct_answer, selected_answer, alphabets_eng, time_taken, is_answer_shown):
    if selected_answer == correct_answer:
        return_value = 'CORRECT'
        if is_answer_shown == 'True':
            return 'Hint Used'
        elif time_taken.total_seconds() < 3:
            correctness = 0.6
        else:
            correctness = 0.9
    else:
        print('answer is wrong')
        return_value = 'WRONG'
        correctness = 1.5

    user_confidence = UserStatsModel.objects.get(user=user)
    existing_confidence_level = getattr(user_confidence, correct_answer)
    new_confidence_level = min(1, existing_confidence_level * correctness)
    if new_confidence_level<0.3 and existing_confidence_level>=0.3:
        try:
            alphabet_counter = getattr(user_confidence, 'alphabet_counter')
            setattr(user_confidence, alphabets_eng[alphabet_counter], 1)
            alphabet_counter+=1
            setattr(user_confidence, 'alphabet_counter', alphabet_counter)
        except:
            pass
    setattr(user_confidence, correct_answer, new_confidence_level)
    user_confidence.save()

    return return_value
