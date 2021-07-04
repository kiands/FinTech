import pandas as pd
import numpy as numpy

import jieba.analyse
## pip install jieba

if __name__ == '__main__':

    df = pd.read_csv('database/stock.csv')
    # print(df)
    # print(df.iloc[0,:])
    # text = df.iloc[0,5]
    # print(text)
    
    jieba.set_dictionary("jieba_dict/dict.txt.big")
    for i in range(len(df)):
        # print(df.iloc[i,7])
        text = df.iloc[i,5]
        tags = jieba.analyse.extract_tags(text, topK=10, withWeight=True)
        for tag, weight in tags:
            print(tag + "," + str(int(weight * 10000)))
        print("-"*10)