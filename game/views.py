import json
import random
from django.apps import apps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

MalayalamAlphabetModel = apps.get_model('home', 'MalayalamAlphabetModel')
previous_selected_question = None

#variables required for ai
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from keras.models import load_model
import numpy as np
import cv2
from django.core.files.base import ContentFile
import uuid
import base64
from django.http import JsonResponse

image_size = 224
model = load_model("keras_model.keras")
counter = 0

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
                pred = model.predict(np.array([image]))
                sign_code = np.argmax(pred[0])
                sign_name = mapper(sign_code)

                correct_answer = previous_selected_question.eng
                if sign_name == correct_answer or counter > 5:
                    reset_counter()
                    result = 'CORRECT'
                    messages.success(request, result)
                    return JsonResponse({'message': result})
                else:
                    increment_counter()
                    result = 'WRONG'
                    return JsonResponse({'message': result})

            except:
                print('error while processing data')
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


## Required Functions

def increment_counter():
    global counter
    counter = counter + 1

def reset_counter():
    global counter
    counter = 0

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
