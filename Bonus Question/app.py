# -*- coding: utf-8 -*-
# @Time : 2025/5/27
# @Author : 侯兆晗
# @Software: PyCharm

import os
import re
import jieba
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 配置
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data/data.csv")
STOPWORDS_PATH = os.path.join(BASE_DIR, "stopwords.txt")
CATEGORY_MAP = {"0": "体育", "1": "国际", "2": "政治", "3": "文化", "4": "社会", "5": "经济"}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# 加载数据
# 跳过表头，指定列名
df = pd.read_csv(DATA_PATH, dtype=str, encoding="utf-8", skiprows=1, names=["category", "news"])
texts = df["news"].tolist()
labels = df["category"].tolist()

# 加载停用词表
with open(STOPWORDS_PATH, encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f if line.strip())

# 定义中英文标点正则，用于过滤
PUNCT_PATTERN = re.compile(
    r"[\u3000-\u303F\uFF00-\uFFEF"
    r"，。！？；：、“”‘’（）《》〈〉【】·—…"
    r"\"'#\$%&\(\)\*\+,\-\./:;<=>\?@\[\]\\\^_`\{\|\}~]"
)

# 分词
def tokenize(text: str):
    # jieba 分词并剔除空串
    tokens = [w for w in jieba.cut(text) if w.strip()]
    # 过滤标点和停用词
    filtered = []
    for w in tokens:
        if PUNCT_PATTERN.fullmatch(w):
            continue
        if w in stopwords:
            continue
        filtered.append(w)
    return filtered

# 训练TF-IDF向量器
vectorizer = TfidfVectorizer(tokenizer=tokenize)
X = vectorizer.fit_transform(texts)

# 搜索接口
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    # 分词
    tokens = tokenize(q)

    # 统计前十高频词
    freq = {}
    for w in tokens:
        freq[w] = freq.get(w, 0) + 1
    top10 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
    top10 = [{"word": w, "count": c} for w, c in top10]

    # 向量化查询并计算相似度
    q_vec = vectorizer.transform([q])
    sims = cosine_similarity(q_vec, X).flatten()
    idxs = sims.argsort()[::-1][:5]
    similar = []
    for i in idxs:
        similar.append({
            "news": texts[i],
            "category": CATEGORY_MAP[labels[i]],
            "score": float(f"{sims[i]:.4f}")
        })

    # 所属类别：最相似文本的类别
    category_of_most_similar = CATEGORY_MAP[labels[idxs[0]]]

    return {
        "tokens": tokens,
        "top10": top10,
        "category": category_of_most_similar,
        "similar": similar
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
