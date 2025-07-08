# -*- coding: utf-8 -*-
# @Time : 2025/5/27
# @Author : 侯兆晗
# @Software: PyCharm

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import numpy as np

catagory = {0:"体育",1:"国际",2:"政治",3:"文化",4:"社会",5:"经济"}


def get_text(path):
    df = pd.read_csv(path)
    text = list(df["news"])
    labels = list(df["category"])
    return (text,labels)


def evaluate(true_labels, predict_labels):
    unique_classes = np.unique(true_labels)
    precision_per_class = []
    recall_per_class = []
    f1_per_class = []
    for cls in unique_classes:
        true_positive = np.sum((true_labels == cls) & (predict_labels == cls))
        false_positive = np.sum((true_labels != cls) & (predict_labels == cls))
        false_negative = np.sum((true_labels == cls) & (predict_labels != cls))

        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        precision_per_class.append(precision)
        recall_per_class.append(recall)
        f1_per_class.append(f1)
    # 计算宏观平均
    precision_macro = np.mean(precision_per_class)

    # 计算微观平均
    true_positive_micro = np.sum([np.sum((true_labels == cls) & (predict_labels == cls)) for cls in unique_classes])
    false_positive_micro = np.sum(
        [np.sum((true_labels != cls) & (predict_labels == cls)) for cls in unique_classes])
    false_negative_micro = np.sum(
        [np.sum((true_labels == cls) & (predict_labels != cls)) for cls in unique_classes])

    precision_micro = true_positive_micro / (true_positive_micro + false_positive_micro)

    # 输出结果
    print("宏观平均: {:.2f}".format(precision_macro))
    print()
    print("微观平均: {:.2f}".format(precision_micro))
    for i, cls in enumerate(unique_classes):
        print("{}: 准确率: {:.2f}, 召回率: {:.2f}, F1分数: {:.2f}".format(catagory[cls], precision_per_class[i], recall_per_class[i], f1_per_class[i]))


train_text,train_label = get_text("train.csv")
test_text,test_label = get_text("test.csv")


vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(train_text)
X_test_tfidf = vectorizer.transform(test_text)
svm = SVC(kernel='linear')
svm.fit(X_train_tfidf, train_label)
y_pred = svm.predict(X_test_tfidf)

evaluate(y_pred,test_label)
