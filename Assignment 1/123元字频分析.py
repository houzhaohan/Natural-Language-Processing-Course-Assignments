
from collections import Counter

with open('侯兆晗.txt', 'r', encoding='utf-8') as f:
    text = f.read().replace('\n', '').replace('/', '')

def sort_items(items):
    return sorted(items.items(), key=lambda x: (-x[1], x[0]))

unigram = Counter(text)

bigram = Counter()
for i in range(len(text) - 1):
    bigram[text[i] + text[i+1]] += 1
    
trigram = Counter()
for i in range(len(text) - 2):
    trigram[text[i] + text[i+1] + text[i+2]] += 1

uni_sorted = sort_items(unigram)
bi_sorted = sort_items(bigram)
tri_sorted = sort_items(trigram)

# 输出到三个独立文件
with open('一元字频.txt', 'w', encoding='utf-8') as f:
    f.write("一元字频次：\n")
    for char, count in uni_sorted:
        f.write(f"{char}: {count}\n")

with open('二元字频.txt', 'w', encoding='utf-8') as f:
    f.write("二元字频次：\n")
    for pair, count in bi_sorted:
        f.write(f"{pair}: {count}\n")

with open('三元字频.txt', 'w', encoding='utf-8') as f:
    f.write("三元字频次：\n")
    for triplet, count in tri_sorted:
        f.write(f"{triplet}: {count}\n")