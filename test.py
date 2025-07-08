def convert_to_intervals(segmented_str):
    words = [word for word in segmented_str.split('/') if word.strip()]
    intervals = []
    current_pos = 1
    for word in words:
        length = len(word)
        end = current_pos + length - 1
        intervals.append([current_pos, end])
        current_pos = end + 1
    return intervals

def main():
    import sys

    def read_lines(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]

    std_lines = read_lines('侯兆晗（校对后）.txt')
    seg_lines = read_lines('侯兆晗.txt')

    if len(std_lines) != len(seg_lines):
        print("错误：文件行数不一致")
        sys.exit(1)

    total_correct = 0
    total_std = 0
    total_seg = 0

    for std_line, seg_line in zip(std_lines, seg_lines):
        std_intervals = convert_to_intervals(std_line)
        seg_intervals = convert_to_intervals(seg_line)

        std_set = set(tuple(interval) for interval in std_intervals)
        seg_set = set(tuple(interval) for interval in seg_intervals)

        correct = len(std_set & seg_set)
        total_correct += correct
        total_std += len(std_intervals)
        total_seg += len(seg_intervals)

    P = total_correct / total_seg if total_seg != 0 else 0
    R = total_correct / total_std if total_std != 0 else 0
    F1 = 2 * P * R / (P + R) if (P + R) != 0 else 0

    print(f"精确率 P: {P:.16f}")
    print(f"召回率 R: {R:.16f}")
    print(f"F测度值: {F1:.16f}")

if __name__ == "__main__":
    main()