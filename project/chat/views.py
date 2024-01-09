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


def receive_chat(request):
    return render(request, 'chat/receive_chat.html')

def give_chat(request):
    return render(request, 'chat/give_chat.html')


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
        "profile_image": user.profile_image_url,  # profile_image 필드가 모델에 존재한다고 가정
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

@login_required
def friend_profile(request, user_id):
    # 사용자 ID를 사용하여 특정 사용자 객체를 가져옵니다.
    user = get_object_or_404(AccountUser, id=user_id)

    # 프로필 페이지에 전달할 컨텍스트를 준비합니다.
    context = {
        "user": user,
        # 필요한 다른 컨텍스트 변수들...
    }

    # 프로필 페이지를 렌더링합니다.
    return render(request, 'chat/friend_profile.html', context)


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
@login_required
@require_POST
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(AccountUser, pk=receiver_id)
    # 이미 요청이 있는지 확인
    if not FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

#  친구 요청 목록 가져오기
@login_required
def fetch_friend_requests(request):
    friend_requests = FriendRequest.objects.filter(receiver=request.user, status='sent')
    requests_data = [{
        'id': fr.id,
        'sender_name': fr.sender.username,
        'sender_profile_image': fr.sender.profile_image.url  # profile_image 필드가 모델에 있다고 가정
    } for fr in friend_requests]
    return JsonResponse({'friend_requests': requests_data})

# 친구 요청 관리
@login_required
@require_POST
def manage_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    if action == 'accept':
        # 친구 요청을 승인하고 친구 관계를 생성합니다.
        Friendship.objects.create(user1=request.user, user2=friend_request.sender)
        friend_request.delete()  # 승인된 친구 요청을 삭제합니다.
    elif action == 'decline':
        # 친구 요청을 거절합니다.
        friend_request.delete()
    return JsonResponse({'success': True})


