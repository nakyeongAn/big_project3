from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def chat(request):
    return render(request, "chat/chat.html")


def account_settings(request):
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


@require_POST  # 요청이 POST 방식인지 확인합니다. 아닐 경우 405 Method Not Allowed 응답을 반환합니다.
@login_required  # 사용자가 로그인한 상태인지 확인합니다. 아닐 경우 로그인 페이지로 리디렉션합니다.
def upload_profile_image(request):
    user = request.user  # 현재 로그인한 사용자 객체를 가져옵니다.
    profile_image = request.FILES.get("profile_picture")  # 요청에서 'profile_picture'라는 이름으로 전송된 파일을 가져옵니다.

    if profile_image:
        # 이미지가 이미 존재하는 경우, 새 이미지로 변경
        if user.profile_image:
            user.profile_image.delete(save=False)  # 기존 이미지를 삭제합니다(데이터베이스에서만 삭제하려면 save=False 사용).
        
        # 새 이미지를 사용자의 profile_image 필드로 설정
        user.profile_image = profile_image
        user.save()  # 변경 사항을 데이터베이스에 저장합니다.

        # 성공적으로 이미지가 저장되었음을 나타내는 JSON 응답을 반환합니다. 새 이미지의 URL도 포함됩니다.
        return JsonResponse({"success": True, "image_url": user.profile_image.url})
    else:
        # 이미지가 제대로 전송되지 않았을 경우, 실패를 나타내는 JSON 응답을 반환합니다.
        return JsonResponse({"success": False, "error": "No image provided"})

def wishlist(request):
    return render(request, "chat/wishlist.html")


def detail(request):
    return render(request, "chat/detail.html")


def friend_profile(request):
    return render(request, "chat/friend_profile.html")


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

# 친구 요청 보내기 뷰 생성

from accounts.models import AccountUser, FriendRequest
@login_required
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(AccountUser, id=receiver_id)
    if request.user != receiver:
        # 이미 요청을 보냈는지 확인
        if not FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
            FriendRequest.objects.create(sender=request.user, receiver=receiver, status='requested')
    return redirect('some_view')  # 요청 후 리다이렉트할 뷰

@login_required
def manage_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    if action == 'accept':
        friend_request.status = 'accepted'
        # 실제 친구 관계를 추가하는 로직을 여기에 구현할 수 있습니다.
    elif action == 'decline':
        friend_request.status = 'declined'
    friend_request.save()
    return redirect('some_view')  # 관리 후 리다이렉트할 뷰
