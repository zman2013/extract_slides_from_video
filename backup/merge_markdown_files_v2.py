import re
import sys

def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def extract_image_descriptions(markdown_content):
    pattern = r"!\[(.*?)\]\((.*?)\)\n((?:[^\n!]*\n?)*)(?=!\[|$)"

    matches = re.findall(pattern, markdown_content, re.MULTILINE)
    print(matches)
    return matches

def merge_descriptions(list1, list2):
    merged = []
    for item1 in list1:
        for item2 in list2:
            if item1[0] == item2[0]:
                merged.append((item1[0], item1[1], item1[2] + "\n" + item2[2]))
                break
        else:
            merged.append(item1)

    for item2 in list2:
        for item1 in list1:
            if item1[0] == item2[0]:
                break
        else:
            merged.append(item2)

    return merged

def write_merged_markdown(merged_list, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for item in merged_list:
            f.write(f"![{item[0]}]({item[1]})\n{item[2]}\n")

if __name__ == "__main__":
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_file_path = sys.argv[3]

    file1_content = read_markdown_file(file1_path)
    file2_content = read_markdown_file(file2_path)

    file1_descriptions = extract_image_descriptions(file1_content)
    file2_descriptions = extract_image_descriptions(file2_content)

    merged_descriptions = merge_descriptions(file1_descriptions, file2_descriptions)

    write_merged_markdown(merged_descriptions, output_file_path)
