from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse

def chat(request):
    return render(request, 'chat/chat.html')

def account_settings(request):
    return render(request, 'chat/account_settings.html')

def profile(request):
    return render(request, 'chat/profile.html')

def wishlist(request):
    return render(request, 'chat/wishlist.html')