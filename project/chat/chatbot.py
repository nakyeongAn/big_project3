import json
from openai import OpenAI

# 챗봇
# secrets.json 파일에서 API 키 읽어오기
with open('secrets.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)
openai_key = secrets["openai_api_key"]

# OpenAI 클라이언트 설정
client = OpenAI(api_key=openai_key)

# 사용자 이름 설정
user_name = "친구 이름"  # 여기에 실제 친구 이름 입력

# JSON 파일로 대화 저장하는 함수 (user의 대화만 저장)
def save_conversation_to_json(conversation, file_name="conversation.json"):
    with open(file_name, 'w', encoding='utf-8') as file:
        user_conversation = [message for message in conversation if message['role'] == 'user']
        json.dump(user_conversation, file, ensure_ascii=False, indent=4)

# 첫 번째 메시지 정의 및 출력
initial_message = f"안녕하세요! {user_name}님을 위한 선물을 준비하고 있는 사람이 있어요. 어떤 종류의 선물을 원하시나요? 예를 들어 음악, 여행, 요리 등 다양한 분야가 있으니까요. 어떤 물건이 가장 원하시는지 알려주세요!"
print(f"Assistant: {initial_message}")

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

while True:
    # 사용자의 입력 받기
    user_input = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")

    if user_input.lower() == 'exit':
        save_conversation_to_json(conversation)
        break

    # 대화 기록에 사용자의 입력 추가
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
    print(f"Assistant: {assistant_response}")
    conversation.append({"role": "assistant", "content": assistant_response})
    save_conversation_to_json(conversation)  # 대화가 추가될 때마다 저장