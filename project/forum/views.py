from django.shortcuts import render

def board(request):
    return render(request, 'forum/board.html')

def notice(request):
    return render(request, 'forum/notice.html')