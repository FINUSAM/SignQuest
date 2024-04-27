from django.shortcuts import render, HttpResponse

# Create your views here.

def learning(request):
    return render(request, 'learning/learning.html')
    return HttpResponse("This is learning Page")