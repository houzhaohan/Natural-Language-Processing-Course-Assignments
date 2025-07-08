# -*- coding: utf-8 -*-
# @Time : 2025/5/27
# @Author : 侯兆晗
# @Software: PyCharm

import os
import pandas as pd
from sklearn.model_selection import train_test_split

catagory = {"体育":"0","国际":"1","政治":"2","文化":"3","社会":"4","经济":"5"}
data = {}

def get_filelist(path):
    filelist = os.listdir(path)
    allfile = []
    for filename in filelist:
        if os.path.isdir(os.path.join(path,filename)):
            filepath = get_filelist(os.path.join(path,filename))
            for items in filepath:
                allfile.append(items)
        else:
            allfile.append(os.path.join(path,filename))
    return allfile

def read_data(path):
    catagory_item = os.path.basename(path).strip('.txt')[-2:]
    catagory_item = catagory[catagory_item]
    with open(path,"r",encoding="utf8") as file:
        input_list = []
        for item in file.readlines():
            if(item != '\n'):
                input_list.append(item.strip("\n"))
            else:
                str_input = " ".join(input_list)
                data[str_input] = catagory_item
                input_list = []

# 读取 CSV 文件
df = pd.read_csv('data/data.csv')

# 打乱数据
df = df.sample(frac=1).reset_index(drop=True)

# 分割数据集（90% 训练集，10% 测试集）
train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)