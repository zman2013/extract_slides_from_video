import argparse
import re
import time
import traceback
from googletrans import Translator
from summarizer import Summarizer
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def truncate_text(text, max_length=512):
    tokens = tokenizer.tokenize(text)
    truncated_tokens = tokens[:max_length]
    return tokenizer.convert_tokens_to_string(truncated_tokens)

def translate_and_summarize(input_file, output_file, start_image):
    # 使用 Google Translate API
    translator = Translator()

    def translate(text):
        while True:
            try:
                translated = translator.translate(text, dest='zh-CN')
                return translated.text
            except Exception as e:
                traceback.print_exc()
                print('retry to translate later')
                time.sleep(3)

    # 使用 BERT 文本摘要库
    summarizer_model = Summarizer()

    def summarize(text):
        while True:
            try:
                # 在调用summarizer_model之前，将文本截断为512个tokens：
                truncated_text = truncate_text(text)
                summary = summarizer_model(truncated_text, ratio=0.2)                
                return summary
            except Exception as e:
                traceback.print_exc()
                print('retry to summarize later')
                time.sleep(3)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    image_blocks = re.split(r'(!\[[^\]]*\]\([^\)]+\))', content)
    translated_blocks = []

    i = 0

    start_translating = False
    with open(output_file, 'a', encoding='utf-8') as f:
        for block in image_blocks:
            if block.strip() == '':
                continue
            
            if block.startswith('!['):  # 图片
                if start_image is None or start_image in block:
                    start_translating = True
                elif start_translating:
                    translated_blocks.append(block)
                    f.write('\n'+block)
                print(block)

            elif start_translating:  # 文本
                translated_text = translate(block)
                if len(translated_text) > 500:
                    summary = summarize(translated_text)
                    translated_blocks.append('summary: '+summary)
                    f.write('\n\n'+'summary: '+summary)
                translated_blocks.append('translated: '+translated_text)
                f.write('\n\n'+'translated: '+translated_text)
                translated_blocks.append('origin: '+block)
                f.write('\n\n'+'origin: '+block)
            
            f.flush()
            
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(translated_blocks))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Translate and summarize a markdown file.")
    parser.add_argument("input_file", help="Path to the input markdown file.")
    parser.add_argument("output_file", help="Path to the output markdown file.")
    parser.add_argument("--start_image", type=str, default=None, help="Start image name to begin translation.")
    args = parser.parse_args()

    translate_and_summarize(args.input_file, args.output_file, args.start_image)
