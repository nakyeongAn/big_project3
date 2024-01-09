from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import chatbot_machine
from accounts.models import AccountUser

def testing(request):
    if request.method == 'POST':
        #폼데이터 및 받는 놈 id 값
        
        occasion = request.POST.get('occasion')
        relationship = request.POST.get('relationship')
        additional_info = request.POST.get('additionalInfo')
        friend_id = request.POST.get('friend_id')

        # 보내는 놈 정보 
        if request.user.is_authenticated:
            print("로그인한 사용자:", request.user.id)
            user_id = request.user.id
        else:
            # 사용자가 로그인하지 않았음
            print("로그인하지 않은 사용자")

        # 결과 값 챗봇 넘기기 
        result = chatbot_machine(friend_id, user_id)
        # 친구페이지로 돌아가버림
        return redirect('chat:friend_profile', id = friend_id)



def chat(request):
    users = AccountUser.objects.filter(is_admin=0)
    return render(request, 'chat/chat.html', {'users':users})

def account_settings(request):
    return render(request, "chat/account_settings.html")


def account_settings(request):
    # ... 프로필 수정 로직
    return render(request, "chat/account_settings.html")


# 프로필 페이지를 위해 수정
@login_required
def profile(request):
    user = request.user
    context = {
        "user": user,
        "username": user.username,
        "user_id": user.member_id,
        "email": user.email,
        "profile_image": user.profile_image,  # profile_image 필드가 모델에 존재한다고 가정
    }
    return render(request, "chat/profile.html", context)


# @require_POST  # 요청이 POST 방식인지 확인합니다. 아닐 경우 405 Method Not Allowed 응답을 반환합니다.
# @login_required  # 사용자가 로그인한 상태인지 확인합니다. 아닐 경우 로그인 페이지로 리디렉션합니다.
# def upload_profile_image(request):
#     user = request.user  # 현재 로그인한 사용자 객체를 가져옵니다.
#     profile_image = request.FILES.get("profile_picture")  # 요청에서 'profile_picture'라는 이름으로 전송된 파일을 가져옵니다.

#     if profile_image:
#         user.profile_image = profile_image  # 사용자의 profile_image 필드를 새로운 이미지로 업데이트합니다.
#         user.save()  # 변경 사항을 데이터베이스에 저장합니다.
#         # 성공적으로 이미지가 저장되었음을 나타내는 JSON 응답을 반환합니다. 새 이미지의 URL도 포함됩니다.
#         return JsonResponse({"success": True, "image_url": user.profile_image.url})
#     # 이미지가 제대로 전송되지 않았을 경우, 실패를 나타내는 JSON 응답을 반환합니다.
#     return JsonResponse({"success": False})


@login_required
@csrf_exempt
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES['profile_picture']:
        user = request.user
        user.profile_image = request.FILES['profile_picture']
        user.save()
        return JsonResponse({'success': True, 'image_url': user.profile_image.url})
    return JsonResponse({'success': False})


def wishlist(request):
    return render(request, "chat/wishlist.html")


def detail(request):
    return render(request, "chat/detail.html")


# def friend_profile(request):
#     return render(request, "chat/friend_profile.html")


# 사용자의 username을 조회
from accounts.models import AccountUser
from django.http import JsonResponse


def search_user(request):
    current_user = request.user
    query = request.GET.get("term", "")  # 쿼리 파라미터에서 검색어 가져오기
    users = AccountUser.objects.filter(username__icontains=query).exclude(username=current_user.username)  # 사용자 이름으로 검색
    results = [{
        'id': user.id,
        'username': user.username,
        'profile_image_url': user.profile_image_url()  # 프로필 이미지 URL 추가
    } for user in users]
    return JsonResponse(results, safe=False)  # JSON 형식으로 반환

# 특정 유저 프로필 확인하기 
def friend_profile(request, id):
    user = get_object_or_404(AccountUser, pk=id)
    return render(request, 'chat/friend_profile.html', {'user':user, 'friend_id': id})

# from accounts.models import AccountUser  # accounts 애플리케이션에서 모델 가져오기
# from accounts.forms import UserEditForm  # accounts 애플리케이션에서 폼 가져오기
# from django.contrib.auth.decorators import login_required

# @login_required
# def edit_user(request):
#     user = get_object_or_404(AccountUser, id=request.user.id)
#     if request.method == 'POST':
#         form = UserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('chat/account_settings.html')  # chat 네임스페이스 사용
#     else:
#         form = UserEditForm(instance=user)

#     return render(request, 'chat/account_settings.html', {'form': form})  # chat 템플릿 경로 사용


