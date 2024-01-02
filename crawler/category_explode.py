import pandas as pd
import ast
import os

# 이미지를 기준으로 파일 불러오기
imgpath='./imgs'
folderlist=os.listdir(imgpath)
for folder in folderlist:
    csv_path=os.path.join('./product_infos/',folder+'_product_infos.csv')
    target_df=pd.read_csv(csv_path)
    # 3단계로 나뉜 카테고리 분해해서 category1, category2, category3에 개별 저장
    target_df['category'] = target_df['category'].apply(ast.literal_eval)
    target_df['category'] = target_df['category'].apply(lambda x:x+[None]*(3-len(x)))
    target_df[['category1', 'category2', 'category3']] = pd.DataFrame(target_df['category'].tolist(), index=target_df.index)
    # 이름 항목에서 필요없는 텍스트 삭제
    target_df['name']=target_df['name'].apply(lambda x:x[:x.find(', 이마트몰')])
    target_df.to_csv(csv_path, index=False)