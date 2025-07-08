def build_vocab(file_path):
    """从已分词语料构建词典并确定最大词长"""
    vocab = set()
    max_len = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            words = line.split('/')
            for word in words:
                if word:  # 过滤空字符串
                    vocab.add(word)
                    current_len = len(word)
                    if current_len > max_len:
                        max_len = current_len
    return vocab, max_len


def max_match(sentence, vocab, max_len):
    """使用最大匹配算法对句子进行分词"""
    tokens = []
    start = 0
    length = len(sentence)
    while start < length:
        end = min(start + max_len, length)
        found = False
        # 从最长可能开始匹配
        for size in range(end - start, 0, -1):
            candidate = sentence[start:start + size]
            if candidate in vocab:
                tokens.append(candidate)
                start += size
                found = True
                break
        if not found:
            # 未找到匹配，切分单字
            tokens.append(sentence[start])
            start += 1
    return tokens


def segment_raw_corpus(raw_path, output_path, vocab, max_len):
    """对生语料进行分词并输出结果"""
    with open(raw_path, 'r', encoding='utf-8') as fin, \
            open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line:  # 处理空行
                fout.write('\n')
                continue
            tokens = max_match(line, vocab, max_len)
            segmented_line = '/'.join(tokens)
            fout.write(segmented_line + '\n')


def main():
    # 输入文件路径
    vocab_file = 'dic.txt'
    raw_file = '侯兆晗.txt'
    output_file = 'output.txt'

    # 构建词典并分词
    vocab, max_len = build_vocab(vocab_file)
    segment_raw_corpus(raw_file, output_file, vocab, max_len)


if __name__ == '__main__':
    main()
