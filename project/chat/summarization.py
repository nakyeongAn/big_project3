import json
from openai import OpenAI
import os
import pickle
import pandas as pd
import torch
from sentence_transformers import util
from django.db import models
from sqlalchemy import create_engine
from django.conf import settings

db_settings = settings.DATABASES['default']
# 챗봇
# secrets.json 파일에서 API 키 읽어오기
# with open('secrets.json', 'r') as secrets_file:
#     secrets = json.load(secrets_file)
# openai_key = secrets["openai_api_key"]

os.environ['OPENAI_API_KEY'] = db_settings['SECRET_KEY']
client = OpenAI()

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

response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
            {
                "role": "system",
                "content": "당신은 문장에서 각 명사가 긍정적인지 부정적인지 분리해주는 똑똑한 사람입니다. \
                문장의 맥락을 고려해 긍정적인 명사와 부정적인 명사로 정확하게 분류하고 출력해주세요. \
                '긍정적인 명사:  부정적인 명사: ' 이런 형태로 출력해줘, '선물', '브랜드', '제품'이라는 단어는 빼줘"
            },
            {
                "role": "user",
                "content": summarization
            }
        ],
        temperature=0.2,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
responses = response.choices[0].message.content

# Split the response into parts and then extract the positive nouns
parts = responses.split('\n')
positive_part = parts[0]  # Assuming the first line contains the positive nouns
positive_nouns_string = positive_part.split(': ')[1]  # Splitting by ': ' to get the list after '긍정적인 명사: '
positive_nouns = positive_nouns_string.split(', ')  # Splitting by ', ' to get individual nouns

# 응답 문자열을 줄 단위로 분리
parts = responses.split('\n')

# 부정적인 명사가 포함된 줄 찾기 (예: "부정적인 명사: 나이키")
negative_part = next(part for part in parts if part.startswith("부정적인 명사"))

# ':' 기호 뒤의 텍스트를 추출하여 부정적인 명사 리스트 생성
negative_nouns_string = negative_part.split(': ')[1]
negative_nouns = negative_nouns_string.split(', ')

# 색상 이름과 해당하는 RGB 코드를 매핑한 딕셔너리
colors_rgb = {
    "빨간색": (255, 0, 0),       # 빨간색의 RGB 코드
    "빨강": (255, 0, 0),       # 빨간색의 RGB 코드
    "주황색": (255, 165, 0),     # 주황색의 RGB 코드
    "노란색": (255, 255, 0),     # 노란색의 RGB 코드
    "노랑": (255, 255, 0),     # 노란색의 RGB 코드
    "초록색": (0, 128, 0),       # 초록색의 RGB 코드
    "파란색": (0, 0, 255),       # 파란색의 RGB 코드
    "남색": (0, 0, 128),         # 남색의 RGB 코드
    "네이비": (0, 0, 128),         # 남색의 RGB 코드
    "보라색": (128, 0, 128),     # 보라색의 RGB 코드
    "흰색": (255, 255, 255),     # 흰색의 RGB 코드
    "하얀색" : (255, 255, 255),     # 흰색의 RGB 코드
    "베이지" : (245,245,220),     # 베이지색의 RGB 코드
    "검정색": (0, 0, 0),         # 검정색의 RGB 코드
    "검은색": (0, 0, 0),         # 검정색의 RGB 코드
    "회색": (128,128,128),         # 회색의 RGB 코드
    "갈색": (139, 69, 19),       # 갈색의 RGB 코드
    "분홍색": (255, 192, 203)    # 분홍색의 RGB 코드
}

# 긍정적인 명사 리스트를 색상 이름에서 RGB 코드로 변환
converted_positive = [colors_rgb[noun] if noun in colors_rgb else noun for noun in positive_nouns]

# 부정적인 명사를 색상 RGB 코드로 변환
converted_negative = [colors_rgb[noun] if noun in colors_rgb else noun for noun in negative_nouns]

matching = []
negative = []
positive_colors = []
negative_colors = []
for i in converted_positive:
  if type(i) == str:
    matching.append(i)
  elif type(i) == tuple:
    positive_colors.append(i)
for i in converted_negative:
  if type(i) == str:
    negative.append(i)
  elif type(i) == tuple:
    negative_colors.append(i)
    

engine = create_engine(f"mysql+pymysql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}")
table_name = "products_product"
# df = pd.read_sql_table(table_name, engine)
# data3 = pd.read_json('all_data_embed.json')
data=pd.read_sql_table(table_name, engine)


# 자신의 드라이브 형식에 맞게 파일 읽
with open('sentencetransformer.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
    
matching_embed = []
for i in matching:
  i_embed = loaded_model.encode(i)
  matching_embed.append(i_embed)
  
def is_number(s):
    """ 문자열이 부동 소수점 숫자 형식인지 확인 """
    try:
        float(s)
        return True
    except ValueError:
        return False

def calculate_score_improved(row, matching, matching_embed, negative, positive_colors, negative_colors, sex, min_price, max_price):
    # 숫자를 문자열로 변환
    category1 = str(row['category1'])
    category2 = str(row['category2'])
    category3 = str(row['category3'])
    name = str(row['name'])

    # 부정적 요소가 있는 경우 점수 계산 제외
    for neg in negative:
        if neg in category1 or neg in category2 or neg in category3 or neg in name:
            return None

    if len(negative_colors) != 0:
        for neg_color in negative_colors:
            neg_red = abs(row['R'] - neg_color[0])
            neg_green = abs(row['G'] - neg_color[1])
            neg_blue = abs(row['B'] - neg_color[2])
            if max(neg_red, neg_green, neg_blue) <= 64:
                return None
            elif sum([neg_red, neg_green, neg_blue]) <= 128:
                return None

    if row['price'] < min_price and row['price'] > max_price:
        return None

    # 긍정적 요소 점수 계산
    score = 0
    for j in matching:
        if j in category1 or j in category2 or j in category3:
            score += 1
        elif j in name:
            score += 1


    for word, word_embed in zip(matching, matching_embed):
        # word_embed를 텐서로 변환 및 차원 조정
        if not isinstance(word_embed, torch.Tensor):
            word_embed = torch.tensor(word_embed, dtype=torch.float)
        word_embed = word_embed.view(1, -1)

        cos_sim_total = 0
        for emb_str in row['embed']:
            # emb가 문자열인 경우 숫자 배열로 변환
            if isinstance(emb_str, str):
                emb_list = emb_str.strip("[]").split(',')
                emb = [float(num) for num in emb_list if is_number(num)]
                emb = torch.tensor(emb, dtype=torch.float)
            elif isinstance(emb_str, torch.Tensor):
                emb = emb_str
            else:
                continue  # emb가 문자열이나 텐서가 아닌 경우

            # 빈 텐서 확인 및 차원 조정
            if emb.nelement() == 0:
                continue
            if len(emb.shape) == 1:
                emb = emb.view(1, -1)

            # word_embed와 emb의 차원이 일치하는지 확인
            if word_embed.shape[1] != emb.shape[1]:
                continue

            cos_sim_ten = util.pytorch_cos_sim(word_embed, emb)
            cos_sim = cos_sim_ten.numpy()[0][0]
            if cos_sim > cos_sim_total:
                cos_sim_total = cos_sim
        score += cos_sim_total

    total = 100 * (score / len(matching))

    if positive_colors == []:
        min_color_diff = 0
    else:
        # 색상 차이 계산
        min_color_diff = float('inf')
        for color in positive_colors:
            pos_red = abs(row['R'] - color[0])
            pos_green = abs(row['G'] - color[1])
            pos_blue = abs(row['B'] - color[2])
            if max(pos_red, pos_green, pos_blue) <= 64:
                min_color_diff = 0
            elif sum([pos_red, pos_green, pos_blue]) <= 128:
                min_color_diff = 0
            color_diff = pos_red + pos_green + pos_blue
            min_color_diff = min(min_color_diff, color_diff)


    # 가장 작은 색상 차이를 30으로 나눈 값을 점수에서 감점
    total -= min_color_diff // 30
    # 'grade' 추가 점수 (현재 주석 처리됨)
    total += row['grade']
    if sex in category1 or sex in category2 or sex in category3 or sex in name:
        total += 0.2

    return total

# DataFrame에 함수 적용
data3['score'] = data3.apply(lambda row: calculate_score_improved(row, matching, matching_embed, negative, positive_colors, negative_colors, sex, min_price, max_price), axis=1)

# 결과 정렬 및 출력
data3_sorted = data3.sort_values(by='score', ascending=False)
data3_sorted[['category', 'name', 'grade', 'score']].head(10)
# data3_sorted.head(10)

