import re

def remove_timestamps_and_merge_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 移除序号、时间戳和空行
    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n')
    content_no_timestamps = re.sub(pattern, '', content)

    # 合并为一个连续的文本字符串
    text = ' '.join(content_no_timestamps.splitlines())

    return text

# 替换为您的 SRT 文件路径
srt_file_path = '/Users/manzhiyuan/workspaces/ndn/video/ndncom/1.srt'
merged_text = remove_timestamps_and_merge_srt(srt_file_path)

# 将提取的文本保存到新的文本文件中
with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(merged_text)

print("Merged text has been saved to output.txt.")
