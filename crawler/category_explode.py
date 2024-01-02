import pandas as pd
import ast
import os

imgpath='./imgs'
folderlist=os.listdir(imgpath)
for folder in folderlist:
    csv_path=os.path.join('./product_infos/',folder+'_product_infos.csv')
    target_df=pd.read_csv(csv_path)
    target_df['category'] = target_df['category'].apply(ast.literal_eval)
    target_df['category'] = target_df['category'].apply(lambda x:x+[None]*(3-len(x)))
    target_df[['category1', 'category2', 'category3']] = pd.DataFrame(target_df['category'].tolist(), index=target_df.index)
    target_df['name']=target_df['name'].apply(lambda x:x[:x.find(', 이마트몰')])
    target_df.to_csv(csv_path, index=False)