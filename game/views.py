from django.shortcuts import render, HttpResponse

# Create your views here.

def game(request):
    return render(request, 'game/game.html')
    return HttpResponse("This is game Page")