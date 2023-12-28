from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse

def list(request):
    return render(request, 'chat/detail.html')

