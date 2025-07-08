def convert_to_tags(segmented_str):
    """将分词结果转换为B、I、E、S标记序列"""
    words = [word for word in segmented_str.split('/') if word.strip()]
    tags = []
    for word in words:
        length = len(word)
        if length == 1:
            tags.append('S')
        else:
            tags.append('B')
            for _ in range(length - 2):
                tags.append('I')
            tags.append('E')
    return tags

def main():
    import sys
    from collections import defaultdict

    def read_lines(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]

    std_lines = read_lines('侯兆晗（校对后）.txt')
    seg_lines = read_lines('侯兆晗.txt')

    if len(std_lines) != len(seg_lines):
        print("错误：文件行数不一致")
        sys.exit(1)

    # 初始化统计字典
    metrics = defaultdict(lambda: {'TP': 0, 'FP': 0, 'FN': 0})

    for idx, (std_line, seg_line) in enumerate(zip(std_lines, seg_lines)):
        std_tags = convert_to_tags(std_line)
        seg_tags = convert_to_tags(seg_line)

        # 检查标记序列长度是否一致
        if len(std_tags) != len(seg_tags):
            print(f"警告：第{idx+1}行字符数不一致，跳过该行")
            continue

        # 统计每个标记的TP、FP、FN
        for std_tag, seg_tag in zip(std_tags, seg_tags):
            for tag in ['B', 'I', 'E', 'S']:
                if std_tag == tag:
                    if seg_tag == tag:
                        metrics[tag]['TP'] += 1
                    else:
                        metrics[tag]['FN'] += 1
                else:
                    if seg_tag == tag:
                        metrics[tag]['FP'] += 1

    # 计算并输出结果
    print("{:<10} {:<10} {:<10} {:<10}".format("标记", "精确率(P)", "召回率(R)", "F1值"))
    for tag in ['B', 'I', 'E', 'S']:
        tp = metrics[tag]['TP']
        fp = metrics[tag]['FP']
        fn = metrics[tag]['FN']

        P = tp / (tp + fp) * 100 if (tp + fp) > 0 else 0.0
        R = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0.0
        F1 = 2 * P * R / (P + R) if (P + R) > 0 else 0.0

        print("{:>10} {:>10.2f}% {:>10.2f}% {:>10.2f}%".format(tag, P, R, F1))

if __name__ == "__main__":
    main()