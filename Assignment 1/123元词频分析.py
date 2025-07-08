import collections

with open('侯兆晗.txt', 'r', encoding='utf-8') as f:
    content = f.read()
words = [word.strip() for word in content.split('/') if word.strip()]

# 统计词频
unigram_counts = collections.Counter(words)
bigrams = zip(words, words[1:])
bigram_counts = collections.Counter(bigrams)
trigrams = zip(words, words[1:], words[2:])
trigram_counts = collections.Counter(trigrams)

# 排序结果
unigram_sorted = unigram_counts.most_common()
bigram_sorted = bigram_counts.most_common()
trigram_sorted = trigram_counts.most_common()

# 分别写入三个文件
with open('一元词频.txt', 'w', encoding='utf-8') as f:
    f.write("一元词频次：\n")
    for word, count in unigram_sorted[:100]:
        f.write(f"{word}: {count}\n")

with open('二元词频.txt', 'w', encoding='utf-8') as f:
    f.write("二元词频次：\n")
    for bigram, count in bigram_sorted[:100]:
        f.write(f"{bigram[0]}{bigram[1]}: {count}\n")

with open('三元词频.txt', 'w', encoding='utf-8') as f:
    f.write("三元词频次：\n")
    for trigram, count in trigram_sorted[:100]:
        f.write(f"{trigram[0]}{trigram[1]}{trigram[2]}: {count}\n")