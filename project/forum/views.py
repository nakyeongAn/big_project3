from django.shortcuts import render

def board(request):
    return render(request, 'forum/board.html')
