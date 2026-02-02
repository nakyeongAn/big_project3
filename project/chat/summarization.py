from openai import OpenAI
from django.conf import settings


def summary(conversation):
    client = OpenAI(api_key=settings.SECRET_OPENAI)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": "사용자의 대화 내용에서 핵심적인 선호도를 파악하고 이를 간결하게 요약해주세요. 선물 준비와 관련된 맥락은 제외하고, 사용자가 언급한 구체적인 선호도(예: 브랜드, 색상, 제품 유형)만을 중심으로 요약합니다."
                },
                {
                    "role": "user",
                    "content": str(conversation)
                }
            ],
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    summarization = response.choices[0].message.content
    return summarization