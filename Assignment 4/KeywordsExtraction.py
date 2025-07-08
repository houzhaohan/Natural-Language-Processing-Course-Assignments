import math
from collections import defaultdict

# 文本预处理函数
def preprocess(text):
    # 定义中文常用标点符号
    chinese_punct = {'，', '。', '！', '？', '；', '：', '“', '”',
                     '‘', '’', '（', '）', '【', '】', '《', '》',
                     '…', '—', '～', '、', '/'}
    # 定义停用词集合
    stop_words = {
        '的', '为', '了', '新', '在', '是', '我', '你', '他', '她', '它',
        '我们', '你们', '他们', '她们', '它们', '这', '那', '上', '下', '不',
        '有', '和', '与', '也', '还', '就', '都', '没', '没有', '要', '说',
        '看', '过', '月', '中', '年', '等', '去', '到', '着', '啊', '呀',
        '吧', '吗', '呢', '哈', '唉', '哦', '噢', '喔', '啦', '嘿', '啰',
        '嘛', '呗', '哼'
    }

    words = text.split('/')
    processed_words = []
    for word in words:
        word = word.strip()
        # 过滤标点和停用词（不再过滤单字符）
        if word and word not in chinese_punct and word not in stop_words:
            processed_words.append(word)
    return processed_words

# 读取并处理目标文档
with open('侯兆晗（校对后）.txt', 'r', encoding='utf-8') as f:
    content = f.read()
processed_doc = preprocess(content)

# 计算TF（词频）
tf = defaultdict(int)
total_words = len(processed_doc)
for word in processed_doc:
    tf[word] += 1

# 读取并处理IDF语料库
document_count = 0
df = defaultdict(int)

with open('202312_check.txt', 'r', encoding='utf-8') as f:
    for line in f:
        document_count += 1
        processed_line = preprocess(line.strip())
        unique_words = set(processed_line)
        for word in unique_words:
            df[word] += 1

# 计算IDF（使用加1平滑）
idf = defaultdict(float)
for word in tf:
    doc_freq = df.get(word, 0)
    idf[word] = math.log((document_count + 1) / (doc_freq + 1)) + 1

# 计算TF-IDF并排序
tfidf_scores = []
for word in tf:
    word_tf = tf[word] / total_words  # 使用归一化TF
    word_idf = idf[word]
    tfidf_scores.append((word, word_tf * word_idf))

# 按得分降序排序
sorted_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

# 输出前10个关键词
print("Top 10 Keywords:")
for i, (word, score) in enumerate(sorted_keywords[:10], 1):
    print(f"{i}. {word} (Score: {score:.4f})")