from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse

def chat(request):
    return render(request, 'chat/chat.html')

def account_settings(request):
    return render(request, 'chat/account_settings.html')

def account_settings(request):
    # ... 프로필 수정 로직
    return render(request, 'chat/account_settings.html')

def profile(request):
    return render(request, 'chat/profile.html')

def wishlist(request):
    return render(request, 'chat/wishlist.html')

def detail(request):
    return render(request, 'chat/detail.html')

def friend_profile(request):
    return render(request, 'chat/friend_profile.html')


# 사용자의 username을 조회
from accounts.models import AccountUser
from django.http import JsonResponse
def search_user(request):
    query = request.GET.get('term', '')  # 쿼리 파라미터에서 검색어 가져오기
    users = AccountUser.objects.filter(username__icontains=query)  # 사용자 이름으로 검색
    results = [{'username': user.username} for user in users]  # 결과 포맷팅
    # results = [{'id': user.id, 'username': user.username, 'image_url': user.profile_image_url} for user in users]  # 결과 포맷팅
    return JsonResponse(results, safe=False)  # JSON 형식으로 반환


