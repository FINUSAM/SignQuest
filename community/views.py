from django.shortcuts import render, HttpResponse

# Create your views here.

def community(request, group='main'):
    return render(request, 'community/community.html')