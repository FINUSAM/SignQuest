import json
import time
import random
from django.apps import apps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

MalayalamAlphabetModel = apps.get_model('home', 'MalayalamAlphabetModel')
UserStatsModel = apps.get_model('account', 'UserStatsModel')
previous_selected_question = None

#variables required for ai
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
#from keras.models import load_model
import numpy as np
import cv2
from django.core.files.base import ContentFile
import uuid
import base64
from django.http import JsonResponse

image_size = 224
#model = load_model("keras_model.keras")
counter_for_ai = 0
counter_for_quiz = 0
score_for_quiz = 0

def mapper(val):
    label_lst = ['A','Aa','Ah','Ai','Am','Au','Ba','Bha','Ca','Cha','D_a','D_ha','Da','Dha','E','E_','Ee','Ee_','Ga','Gha','Ha','I','Ii','Ilh','Ill','In','Inh','Irr','Ja','Ka','Kha','La','Lha','Ma','N_a','Na','Nga','Nha','Nothing','O','Oo','Pa','Pha','R','Ra','Rha','Sa','Sha','Shha','Space','T_a','T_ha','Ta','Tha','U','U_','Uu','Uu_','Va','Ya','Zha']
    NUM_CLASSES = len(label_lst)
    REV_CLASS_MAP = {i:label_lst[i] for i in range(NUM_CLASSES)}
    return REV_CLASS_MAP[val]

# Create your views here.

@login_required
def game(request):
    games = ['flashcard', 'ordering', 'quiz']
    return render(request, 'game/game.html', {'games':games})

@login_required
def flashcard_levels(request): 
    if request.method == 'POST':
        if request.content_type == 'application/json':
            received_data = request.body.decode()
            json_data = json.loads(received_data)
            level = json_data.get('level').strip()
            score = json_data.get('score')
            user_stats = UserStatsModel.objects.get(user=request.user)
            if getattr(user_stats, 'flashcard_' + level)==0 or getattr(user_stats, 'flashcard_' + level)>score:
                setattr(user_stats, 'flashcard_' + level, score)
                if getattr(user_stats, 'flashcard_allowed_levels') == int(level):
                    setattr(user_stats, 'flashcard_allowed_levels', int(level)+1)
                user_stats.save()
            return JsonResponse({'message': 'Score saved successfully'})
        else:
            return JsonResponse({'message': 'Something went wrong'})
        
    no_of_levels = UserStatsModel.objects.get(user=request.user).flashcard_allowed_levels
    return render(request, 'game/flashcard_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def flashcard(request, level):
    allowed_levels = UserStatsModel.objects.get(user=request.user).flashcard_allowed_levels
    if level > allowed_levels:
        return redirect('flashcard_levels')
    all_alphabets = MalayalamAlphabetModel.objects.all()
    user_stats = UserStatsModel.objects.get(user=request.user)
    highscore = getattr(user_stats, 'flashcard_' + str(level))
    alphabet_list = {}
    for alphabet in all_alphabets:
        alphabet_list[alphabet.mal] = alphabet.image.url
    return render(request, 'game/flashcard.html', {'level':level, 'alphabet_list':alphabet_list, 'highscore':highscore})

@login_required
def ordering_levels(request):
    no_of_levels = 2
    return render(request, 'game/ordering_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def ordering_alphabet(request):
    user_stats = UserStatsModel.objects.get(user=request.user)
    if request.method == 'POST':
        if request.content_type == 'application/json':
            received_data = request.body.decode()
            json_data = json.loads(received_data)
            score = json_data.get('score')
            user_stats = UserStatsModel.objects.get(user=request.user)
            existing_highscore = getattr(user_stats, 'ordering_alphabet')
            if existing_highscore==0 or existing_highscore>score:
                setattr(user_stats, 'ordering_alphabet', score)
                user_stats.save()
            return JsonResponse({'message': 'Score saved successfully'})
        else:
            return JsonResponse({'message': 'Something went wrong'})
    
    all_alphabets = MalayalamAlphabetModel.objects.all()
    existing_highscore = getattr(user_stats, 'ordering_alphabet')
    alphabet_list = []
    for alphabet in all_alphabets:
        alphabet_list.append(alphabet.mal)
    return render(request, 'game/ordering alphabet.html', {'alphabet_list':alphabet_list, 'highscore': existing_highscore})

@login_required
def ordering_image(request):
    user_stats = UserStatsModel.objects.get(user=request.user)
    if request.method == 'POST':
        if request.content_type == 'application/json':
            received_data = request.body.decode()
            json_data = json.loads(received_data)
            score = json_data.get('score')
            user_stats = UserStatsModel.objects.get(user=request.user)
            existing_highscore = getattr(user_stats, 'ordering_image')
            if existing_highscore==0 or existing_highscore>score:
                setattr(user_stats, 'ordering_image', score)
                user_stats.save()
            return JsonResponse({'message': 'Score saved successfully'})
        else:
            return JsonResponse({'message': 'Something went wrong'})

    all_alphabets = MalayalamAlphabetModel.objects.all()
    existing_highscore = getattr(user_stats, 'ordering_image')
    alphabet_list = []
    for alphabet in all_alphabets:
        alphabet_list.append(alphabet.image.url)
    return render(request, 'game/ordering_image.html', {'alphabet_list':alphabet_list, 'highscore': existing_highscore})

@login_required
def quiz_levels(request):
    no_of_levels = 3
    return render(request, 'game/quiz_levels.html', {'total_levels': range(1,no_of_levels+1)})

@login_required
def quiz_normal(request, level):
    user_stats = UserStatsModel.objects.get(user=request.user)
    highscore_var = 'quiz_' + str(level)
    highscore = getattr(user_stats, highscore_var)

    if request.method == 'POST':
        selected_answer = request.POST.get('selected-answer')
        correct_answer = previous_selected_question.eng
        if selected_answer == correct_answer:
            result = "CORRECT"
            increment_counter_for_quiz(1)
        else:
            result = "WRONG"
            increment_counter_for_quiz(0)
        messages.success(request, result)
        return redirect('quiz_normal', level)
    
    if counter_for_quiz < 20:

        all_alphabets = MalayalamAlphabetModel.objects.all()
        current_selected_question = selectRandomQuestion(all_alphabets)
        selected_options = getRandomOptions(all_alphabets, current_selected_question)

        if level == 2:
            data = {
                'currentscore':score_for_quiz,
                'highscore': highscore,
                'question': current_selected_question.mal,
                'options':[{'eng':option.eng, 'image':option.image.url} for option in selected_options]
            }
        elif level == 1:
            data = {
                'currentscore':score_for_quiz,
                'highscore': highscore,
                'question': current_selected_question.image.url,
                'options':[{'eng':option.eng, 'mal':option.mal} for option in selected_options]
            }
        else:
            redirect('quiz_levels')
    
    else:
        if score_for_quiz > highscore:
            setattr(user_stats, highscore_var, score_for_quiz)
            user_stats.save()
            highscore = score_for_quiz
        data = {
            'currentscore':score_for_quiz,
            'highscore':highscore,
            'finish':'true'
        }
        reset_counter_for_quiz()

    return render(request, 'game/quiz_normal.html', data)

def quiz_ai_main(request):
        return render(request, 'game/quiz_ai.html')

def quiz_ai(request):
    if request.method == "GET":
        all_alphabets = MalayalamAlphabetModel.objects.all()
        current_selected_question = selectRandomQuestion(all_alphabets)
        return JsonResponse({'question': current_selected_question.mal})
    elif request.method == "POST":
        if request.content_type == 'application/json':
            try:
                received_data = request.body.decode()
                json_data = json.loads(received_data)
                image_data_uri = json_data.get('imageData')
                encoded_image_data = image_data_uri.split(',')[1]
                decoded_image_data = base64.b64decode(encoded_image_data)
                nparr = np.frombuffer(decoded_image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (image_size, image_size))
                #pred = model.predict(np.array([image]))
                #sign_code = np.argmax(pred[0])
                sign_name = mapper('a')#sign_code)

                correct_answer = previous_selected_question.eng
                if sign_name == correct_answer or counter_for_ai > 5:
                    reset_counter_for_ai()
                    result = 'CORRECT'
                    messages.success(request, result)
                    return JsonResponse({'message': result})
                else:
                    increment_counter_for_ai()
                    result = 'WRONG'
                    return JsonResponse({'message': result})

            except:
                print('error while processing data')
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


## Required Functions

def increment_counter_for_ai():
    global counter_for_ai
    counter_for_ai = counter_for_ai + 1

def reset_counter_for_ai():
    global counter_for_ai
    counter_for_ai = 0

def increment_counter_for_quiz(score):
    global counter_for_quiz
    global score_for_quiz
    counter_for_quiz = counter_for_quiz + 1
    score_for_quiz = score_for_quiz + score

def reset_counter_for_quiz():
    global counter_for_quiz
    global score_for_quiz
    counter_for_quiz = 0
    score_for_quiz = 0

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
