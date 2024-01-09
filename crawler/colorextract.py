import numpy as np
import pandas as pd
from colorthief import ColorThief
import os
# 이미지를 기준으로 읽어올 파일 이름 지정
imgpath='./imgs'
folderlist=os.listdir(imgpath)

for folder in folderlist:
    # 각 폴더 내 이미지 파일 불러오기
    result=[]
    imglist=os.listdir(imgpath+'/'+folder)
    for img in imglist:
        # 개별 이미지 대표 색 5개 추출 후 대표색만 RGB HEX코드로 저장
        now_img_path=os.path.join(imgpath+'/'+folder, img)
        color_check=ColorThief(now_img_path)
        palette=color_check.get_palette(color_count=5)
        result.append([format(palette[0][0],'X')+format(palette[0][1],'X')+format(palette[0][2],'X')])
    #기존 CSV 파일에 컬러 추출 결과 저장
    color_array=np.array(result)
    color_pd=pd.DataFrame(color_array, columns=['RGB_Code'])
    csv_path=os.path.join('./product_infos/',folder+'_product_infos.csv')
    data=pd.read_csv(csv_path)
    data=pd.concat([data, color_pd], axis=1)
    data.to_csv(csv_path, index=False)