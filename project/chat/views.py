from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def chat(request):
    return render(request, 'chat/chat.html')

def account_settings(request):
    return render(request, 'chat/account_settings.html')

def account_settings(request):
    # ... 프로필 수정 로직
    return render(request, 'chat/account_settings.html')

# def profile(request):
#     return render(request, 'chat/profile.html')

#프로필 페이지를 위해 수정
@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'username': user.username,
        'user_id': user.member_id,
        'email': user.email,
        # 'profile_image': user.profile_image,  # profile_image 필드가 모델에 존재한다고 가정
    }
    return render(request, 'chat/profile.html', context)


@require_POST
@login_required
def upload_profile_image(request):
    user = request.user
    profile_image = request.FILES.get('profile_picture')
    if profile_image:
        user.profile_image = profile_image  # profile_image 필드 업데이트
        user.save()
        return JsonResponse({'success': True, 'image_url': user.profile_image.url})
    return JsonResponse({'success': False})

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


