from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import FriendRequest, Friendship, Conversation, GiftRequest, Three
from accounts.models import AccountUser
from django.db.models import Q
from .forms import CustomedUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from .summarization import summary

from openai import OpenAI
import json
from .models import *


# 챗봇 사용자 대답 저장
@require_POST
def send_message(request):
    data = json.loads(request.body)
    message_text = data.get('message')
    if message_text:
        # 'user_content' 필드에 메시지 저장
        Message.objects.create(user_content=message_text, user=request.user)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No message text provided'})


def receive_chat(request):
    context = {}

    # 사용자가 로그인한 경우에만 gift_requests 정보를 가져옵니다.
    if request.user.is_authenticated:
        user_id = request.user.id
        gift_requests = GiftRequest.objects.filter(receiver=user_id)
        context['gift_requests'] = gift_requests
        context['has_chat_gift_request'] = gift_requests.exists()
        account_user = AccountUser.objects.get(id=user_id)
        context['username'] = account_user.username
    return render(request, 'chat/receive_chat.html', context)


def give_chat(request):
    context = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        gift_requests = GiftRequest.objects.filter(sender=user_id)

        # receiver id를 사용하여 각 AccountUser를 조회하고 이름을 저장
        gift_receiver_usernames = {}
        for gr in gift_requests:
            receiver_id = str(gr.receiver)
            receiver_user = AccountUser.objects.get(id=receiver_id)
            gift_receiver_usernames[receiver_id] = receiver_user.username

        context['gift_requests'] = gift_requests
        context['has_chat_gift_request'] = gift_requests.exists()
        context['gift_receiver'] = receiver_user
        context['three_list'] = []

    return render(request, 'chat/give_chat.html', context)


# 프로필 페이지를 위해 수정
@login_required
def profile(request):
    user = request.user
    context = {
        "user": user,
        "username": user.username,
        "user_id": user.member_id,
        "email": user.email,
        "profile_image": user.profile_image_url,
    }
    return render(request, "chat/profile.html", context)


def account_settings(request):
    return render(request, "chat/account_settings.html")


@login_required
@csrf_exempt
def upload_profile_image(request):
    user = request.user
    profile_image = request.FILES.get("profile_picture")

    if profile_image:
        if user.profile_image:
            user.profile_image.delete(save=False)

        user.profile_image = profile_image
        user.save()

        return JsonResponse({"success": True, "image_url": user.profile_image.url})
    else:
        return JsonResponse({"success": False, "error": "No image provided"})

def wishlist(request):
    return render(request, "chat/wishlist.html")


def detail(request):
    return render(request, "chat/detail.html")

# 친구 등록되어있는지 확인
@login_required
def friend_profile(request, user_id):
    user = get_object_or_404(AccountUser, id=user_id)
    is_friend = Friendship.objects.filter(
        (Q(user1=request.user) & Q(user2=user)) | (Q(user1=user) & Q(user2=request.user))
    ).exists()

    context = {
        "user": user,
        "is_friend": is_friend,
        "username" : user.username
    }

    return render(request, 'chat/friend_profile.html', context)

# 폼데이터 받기
def giftform(request):
    if request.method == 'POST':
        occasion = request.POST.get('occasion')
        relationship = request.POST.get('relationship')
        additional_info = request.POST.get('additionalInfo')
        minAmount = request.POST.get('minAmount')
        maxAmount = request.POST.get('maxAmount')
        friend_id = request.POST.get('friend_id')
        user_id = request.user.id

        result=GiftRequest(sender=user_id, receiver=friend_id, additionalinfo=additional_info, minamount=minAmount, maxamount=maxAmount, relationship=relationship, occasion=occasion, is_completed=False)
        result.save()
        return redirect('chat:friend_profile', user_id=friend_id)


# 사용자의 username을 조회
def search_user(request):
    current_user = request.user
    query = request.GET.get("term", "")
    users = AccountUser.objects.filter(username__icontains=query).exclude(username=current_user.username)
    results = [{
        'id': user.id,
        'username': user.username,
        'profile_image_url': user.profile_image_url()
    } for user in users]
    return JsonResponse(results, safe=False)

# 친구 요청 보내기 뷰 생성
@login_required
@require_POST
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(AccountUser, pk=receiver_id)
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
        'sender_profile_image': fr.sender.profile_image.url
    } for fr in friend_requests]
    return JsonResponse({'friend_requests': requests_data})

# 친구 요청 관리
@login_required
@require_POST
def manage_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    if action == 'accept':
        Friendship.objects.create(user1=request.user, user2=friend_request.sender)
        friend_request.delete()
    elif action == 'decline':
        friend_request.delete()
    return JsonResponse({'success': True})

# 선물정보데이터 보내버리기
def fetch_gift_requests(request):
    gift_requests=GiftRequest.objects.filter(receiver=request.user.id)
    receiver_user = AccountUser.objects.filter(id = request.user.id)
    requests_data = [{
        'id' : gr.id,
        'gender' : receiver_user[0].gender,
        'additionalinfo' : gr.additionalinfo,
        'minamount' : gr.minamount,
        'maxamount' : gr.maxamount,
        'relationship' : gr.relationship,
        'occasion' : gr.occasion
    } for gr in gift_requests]
    return JsonResponse({'gift_requests' : requests_data})

#챗봇
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        receiver=AccountUser.objects.filter(id = request.user.id)[0]
        gender=receiver.gender
        gift_requests=GiftRequest.objects.filter(receiver=request.user.id)
        data={'gender':gender,'min':gift_requests[0].minamount, 'max':gift_requests[0].maxamount, 'receiver':request.user.id}
        response = chatbot_machine(message, data)

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'receive_chat')


# OpenAI 클라이언트 설정
client = OpenAI(api_key=settings.SECRET_OPENAI)

# 첫 번째 메시지 정의
initial_message = f"안녕하세요! 너님을 위한 선물을 준비하고 있는 사람이 있어요. 어떤 종류의 선물을 원하시나요? 예를 들어 음악, 여행, 요리 등 다양한 분야가 있으니까요. 어떤 물건이 가장 원하시는지 알려주세요!"


# 대화 기록을 저장할 리스트 초기화
conversation = [
    {
        "role": "system",
        "content": "누군가에게 선물을 주기 위해 그 사람의 취향을 알아보려고 해. 하지만 선물 받는 당사자에게 직접 물어보기 어려워서 너를 이용해서 익명으로 선물을 받는 상대에게 물어보려고 해. 너는 상대방에게 구체적으로 어떤 취향을 갖고 있는지 물어보고, 취향을 파악해주는 조수야. 너는 상대방의 이름, 나이, 성별을 알고 있어. 제일 첫 대화는 인사와 함께 상대방에게 갖고 싶은 물건이 있는지 물어봐줘야 해. 누군가가 상대방을 위해 선물을 준비하고 있다는 사실을 알려줘. 상대방에게 답변이 오면 구체적인 품목에 대한 선호도 질문을 해야해. 상대방이 이미 선호하는 품목을 언급했다면, 그 품목에 대해 더 자세히 물어볼 수 있어. 최대 3문장으로 말해줘."
    },
    {
        "role": "assistant",
        "content": initial_message
    }
]

def chatbot_machine(message, userdata):
    user_input = message

    if user_input.lower() == '고마워':
        summary_text = summary(conversation)
        gift_requests = GiftRequest.objects.filter(receiver=userdata['receiver'])
        if gift_requests.exists():
            gift_request = gift_requests.first()
            gift_request.is_completed = True
            gift_request.save()
        return "대화가 종료되었습니다."

    conversation.append({"role": "user", "content": user_input})
    # 챗봇에게 대화 전달 및 응답 받기
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8c5qJUIG",
        messages=conversation,
        max_tokens=150,
        temperature=0.4,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 챗봇의 응답을 대화 기록에 추가 및 출력
    assistant_response = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_response})
    return assistant_response


from django.contrib.auth.forms import UserChangeForm

def account_settings(request):
    return render(request, "chat/account_settings.html")


def update(request):
    if request.method == "POST":
        form = CustomedUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('chat:account_settings')
    else:
        form =CustomedUserChangeForm(instance=request.user)
    content = {'form' : form}
    return render(request, 'chat/update.html', content)

def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('chat:account_settings')
    else:
        form =PasswordChangeForm(request.POST)
    content = {'form' : form}
    return render(request, 'chat/password_change.html', content)