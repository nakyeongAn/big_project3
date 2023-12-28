from django.shortcuts import render

def signup(request):
    return render(request, 'registration/signup.html')

def login(request):
    return render(request, 'registration/login.html')

def cancel(request):
    return render(request, 'registration/cancel.html')