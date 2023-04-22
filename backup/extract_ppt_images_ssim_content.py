import cv2
import numpy as np
import ffmpeg
from skimage.metrics import structural_similarity as ssim
import pytesseract

def contains_ppt_content(image):
    # 对图像进行OCR识别
    text = pytesseract.image_to_string(image)

    # 设置一个识别到的字符数量阈值，根据需要调整
    character_threshold = 30
    length = len(text)
    print(f'{length}:{text}')

    blacklist = ['cysers', 'excettence', 'cysersecurity', 'cybersecurity', 'excellence', 'coe', 'exceience', 'eRsecurity', 'national', 'soe', 'soc', 'coc', 'cae', 'exceluence', 'excelience']
    if any(word in text.lower() for word in blacklist):
        return False

    # 如果识别到的字符数量大于阈值，则认为图像包含PPT内容
    return len(text) > character_threshold

def extract_ppt_frames(video_file, similarity_threshold=0.90):
    video = cv2.VideoCapture(video_file)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))

    prev_frame = None
    unique_frames = []

    for i in range(frame_count):

        if len(unique_frames) > 10:
            break

        ret, frame = video.read()
        if not ret:
            break

        if not contains_ppt_content(frame):
            continue

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            prev_frame = gray_frame
            unique_frames.append((i, frame))
            continue

        similarity = ssim(gray_frame, prev_frame, full=True, multichannel=False)[0]

        if similarity < similarity_threshold:
            unique_frames.append((i, frame))
            prev_frame = gray_frame

    video.release()
    return unique_frames, fps


def save_extracted_frames(output_dir, unique_frames, fps):
    for i, (frame_idx, frame) in enumerate(unique_frames):
        timestamp = frame_idx / fps
        file_name = f"{output_dir}/ppt_frame_{i}_time_{timestamp:.2f}.png"
        cv2.imwrite(file_name, frame)


if __name__ == "__main__":
    video_file = "/Users/manzhiyuan/log/video/NDNComm_2023_NIST_1.mp4"
    output_dir = "/Users/manzhiyuan/log/video/5"

    unique_frames, fps = extract_ppt_frames(video_file)
    save_extracted_frames(output_dir, unique_frames, fps)
