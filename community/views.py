from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def community(request, group='main'):
    return render(request, 'community/community.html')