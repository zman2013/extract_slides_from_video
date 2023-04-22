import argparse
import re
import openai
import time
import traceback

def translate_and_summarize(input_file, output_file, start_image):
    def translate(text):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content": f"Translate the following English text to Chinese:\n\n{text}"},
                        ]
                    )
            
                return response['choices'][0]['message']['content'].strip()
            except Exception as e:
                traceback.print_exc()
                print('retry to translate later')
                time.sleep(3)


    def summarize(text):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content": f"Write a brief summary of the following English text in Chinese:\n\n{text}"},
                        ]
                    )
                return response['choices'][0]['message']['content'].strip()
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
                if start_translating:
                    translated_blocks.append(block)
                    f.write('\n'+block)
                print(block)

            elif start_translating:  # 文本
                
                if len(block) > 2000:
                    summary = summarize(block)
                    translated_blocks.append('summary: '+summary)
                    f.write('\n\n'+'summary: '+summary)
                else:
                    translated_text = translate(block)
                    translated_blocks.append('translated: '+translated_text)
                    f.write('\n\n'+'translated: '+translated_text)

                translated_blocks.append('origin: '+block)
                f.write('\n\n'+'origin: '+block)
            
            f.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Translate and summarize a markdown file.")
    parser.add_argument("input_file", help="Path to the input markdown file.")
    parser.add_argument("output_file", help="Path to the output markdown file.")
    parser.add_argument("--start_image", default=None, help="Start image name to begin translation.")
    args = parser.parse_args()

    translate_and_summarize(args.input_file, args.output_file, args.start_image)
