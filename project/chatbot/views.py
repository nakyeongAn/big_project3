from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import json
# Create your views here.

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # 대화 상태 체크
        # if request.session.get('chat_state') == 'ended':
        #     return JsonResponse({'message': message, 'response': '대화가 이미 종료되었습니다.'})

        # if message.lower() == 'exit':
        #     request.session['chat_state'] = 'ended'
        #     return JsonResponse({'message': message, 'response': '대화가 종료되었습니다.'})

        response = chatbot_machine(message)
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html')

def chatbot_machine(message):

    with open('secrets.json', 'r') as secrets_file:
        secrets = json.load(secrets_file)
    openai_key = secrets["openai_key"]

    # OpenAI 클라이언트 설정
    client = OpenAI(api_key=openai_key)
    
    conversation_history = [
        # 기존의 내용들
    ]
    # 첫 번째 메시지 정의
    initial_message = f"안녕하세요! 너님을 위한 선물을 준비하고 있는 사람이 있어요. 어떤 종류의 선물을 원하시나요? 예를 들어 음악, 여행, 요리 등 다양한 분야가 있으니까요. 어떤 물건이 가장 원하시는지 알려주세요!"


    # 대화 기록을 저장할 리스트 초기화
    conversation = [
        {
            "role": "system",
            "content": "누군가에게 선물을 주기 위해 그 사람의 취향을 알아보려고 해. 하지만 선물 받는 당사자에게 직접 물어보기 어려워서 너를 이용해서 익명으로 선물을 받는 상대에게 물어보려고 해. 너는 상대방에게 구체적으로 어떤 취향을 갖고 있는지 물어보고, 취향을 파악해주는 조수야. 너는 상대방의 이름, 나이를 알고 있어. 제일 첫 대화는 인사와 함께 상대방에게 갖고 싶은 물건이 있는 물어봐줘야 해. 누군가가 상대방을 위해 선물을 준비하고 있다는 사실을 알려줘. 상대방에게 답변이 오면 구체적인 품목에 대한 선호도 질문을 해야해. 상대방이 이미 선호하는 품목을 언급했다면, 그 품목에 대해 더 자세히 물어볼 수 있어. 최대 3문장으로 말해줘."
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
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=150,
        temperature=0.4,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 챗봇의 응답을 대화 기록에 추가 및 출력
    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

