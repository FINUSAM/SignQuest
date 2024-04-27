from django.shortcuts import render, HttpResponse

# Create your views here.

def account(request):
    return render(request, "account/account.html")
    return HttpResponse("This is account Page")

def login_view(request):
    return HttpResponse("This is login Page")

def logout_view(request):
    return HttpResponse("This is logout Page")

def signup_view(request):
    return HttpResponse("This is signup Page")