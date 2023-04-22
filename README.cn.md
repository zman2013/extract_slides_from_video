[English](README.md) | 简体中文

# extract_slides_from_video
这是一个用于从会议视频中提取幻灯片并为每张幻灯片添加对应文本的项目。项目包含三个脚本：`extract_ppt_images_ssim_ocr.py`，`create_markdown.py` 和 `translate.py`。

## 项目使用步骤
1. 使用 extract_ppt_images_ssim_ocr.py 从会议视频中提取幻灯片。
2. 使用 create_markdown.py 为提取的幻灯片创建一个 Markdown 文件。
3. 使用 translate.py 翻译和总结 Markdown 文件中的文本。

### extract_ppt_images_ssim_ocr.py

这个脚本用于从会议视频中提取幻灯片。它利用结构相似性(SSIM)和OCR技术找出视频中的幻灯片，并将其保存为图片。

### create_markdown.py

这个脚本用于为提取的幻灯片图片创建一个markdown文件。它会将字幕文件(.srt)中与图片对应的文本添加到markdown文件中。

### translate.py

这个脚本用于翻译和摘要markdown文件。它使用OpenAI GPT-3.5-turbo模型将英文文本翻译成中文，并为较长的文本生成摘要。

## 使用方法

1. 首先，使用`extract_ppt_images_ssim_ocr.py`从会议视频中提取幻灯片图片：
   
```bash
python extract_ppt_images_ssim_ocr.py <video_file> <output_dir> [--start_time START_TIME] [--end_time END_TIME]
```


2. 接着，使用`create_markdown.py`为提取的图片创建一个markdown文件：

```bash
python create_markdown.py <folder> <video> <output>
```


其中`<folder>`是包含提取的幻灯片图片和字幕文件的文件夹，`<video>`是会议视频文件，`<output>`是要生成的markdown文件。

3. 最后，使用`translate.py`翻译和摘要markdown文件：

```bash
python translate.py <input_file> <output_file> [--start_image START_IMAGE]
```

其中`<input_file>`是由`create_markdown.py`生成的markdown文件，`<output_file>`是要生成的翻译后的markdown文件。可以使用`--start_image`选项指定从哪张图片开始翻译。

注：在使用`translate.py`之前，请确保已经配置好OpenAI的API密钥。

确保您已经配置了您的 OpenAI API 密钥。您可以将 API 密钥添加到您的环境变量中，如下所示：
```bash
export OPENAI_API_KEY="your_api_key_here"
```

4. [optional] 如果使用 VS Code，可以安装 Pandoc 插件将 markdown 导出为 pdf、word、html等格式。