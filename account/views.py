from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def account(request):
    return render(request, "account/account.html")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', reverse('home'))
                return redirect(next_url)  # Redirect to home page after successful login
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home') 

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   # Redirect to home page after successful signup
    else:
        if request.user.is_authenticated:
            return redirect('login')
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})