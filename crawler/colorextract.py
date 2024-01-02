import numpy as np
import pandas as pd
from colorthief import ColorThief
import os

imgpath='./imgs'
folderlist=os.listdir(imgpath)

for folder in folderlist:
    result=[]
    imglist=os.listdir(imgpath+'/'+folder)
    for img in imglist:
        now_img_path=os.path.join(imgpath+'/'+folder, img)
        color_check=ColorThief(now_img_path)
        palette=color_check.get_palette(color_count=5)
        result.append([format(palette[0][0],'X')+format(palette[0][1],'X')+format(palette[0][2],'X')])
    color_array=np.array(result)
    color_pd=pd.DataFrame(color_array, columns=['RGB_Code'])
    csv_path=os.path.join('./product_infos/',folder+'_product_infos.csv')
    data=pd.read_csv(csv_path)
    data=pd.concat([data, color_pd], axis=1)
    data.to_csv(csv_path, index=False)