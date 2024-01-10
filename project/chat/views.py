from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import FriendRequest, Friendship
from django.db.models import Q

from openai import OpenAI
import os
import json
from .models import * 
from accounts.models import AccountUser

# 챗봇 사용자 대답 db에 저장
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
    user = get_object_or_404(AccountUser, id=user_id)
    is_friend = Friendship.objects.filter(
        (Q(user1=request.user) & Q(user2=user)) | (Q(user1=user) & Q(user2=request.user))
    ).exists()
    

    context = {
        "user": user,
        "is_friend": is_friend,
        # 기타 필요한 컨텍스트 변수들...
    }

    return render(request, 'chat/friend_profile.html', context)

def giftform(request):
    if request.method == 'POST':
        #폼데이터 및 받는 놈 id 값
        
        occasion = request.POST.get('occasion')
        relationship = request.POST.get('relationship')
        additional_info = request.POST.get('additionalInfo')
        minAmount = request.POST.get('minAmount')
        maxAmount = request.POST.get('maxAmount') 
        friend_id = request.POST.get('friend_id')
        print(occasion, relationship, additional_info, minAmount, maxAmount, '친구 id ',friend_id)
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
        return redirect('chat:friend_profile', user_id = friend_id)



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


#챗봇
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        response = chatbot_machine(message)
        
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'receive_chat')


def chatbot_machine(friend_id, user_id):
  #  user_name = input("이름 : ")  # 여기에 실제 친구 이름 입력

    # # 성별 입력
    # sex = input("성별 : ") # 성별 입력
    # not_sex = " "
    # if sex == "여성":
    #     not_sex = "남성"
    # else:
    #     not_sex = "여성"
    
    # db_settings = settings.DATABASES['default']
    with open('secrets.json', 'r') as secrets_file:
        secrets = json.load(secrets_file)
    openai_key = secrets["openai_key"]

    # # OpenAI 클라이언트 설정
    client = OpenAI(api_key=openai_key)
    # db_settings = settings.DATABASES['default']
    # os.environ['OPENAI_API_KEY'] = db_settings['SECRET_OPENAI']
    # client = OpenAI()

    
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
    user_input = message

    if user_input.lower() == 'exit':
        # 디비에 저장을 시키고 status 바꾸면 됨
        return "대화가 종료되었습니다. "
    
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
    print('response ', response)
    print('assistant_response ',assistant_response)
    print('conversation ',conversation)
    print('==========================================')
    return assistant_response