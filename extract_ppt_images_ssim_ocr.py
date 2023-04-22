import cv2
import argparse
from skimage.metrics import structural_similarity as ssim
import pytesseract

def contains_ppt_content(image):

    text = pytesseract.image_to_string(image)

    character_threshold = 20
    length = len(text)
    print(f'{length}:{text}')

    blacklist = ['cysers', 'excettence', 'cysersecurity', 'cybersecurity', 'excellence', 'coe', 'exceience', 'eRsecurity', 'national', 'soe', 'soc', 'coc', 'cae', 'exceluence', 'excelience']
    if any(word in text.lower() for word in blacklist):
        return False

    return len(text) > character_threshold

def extract_ppt_frames(video_file, similarity_threshold=0.95, start_time=0, end_time=None):
    video = cv2.VideoCapture(video_file)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    start_frame = int(start_time * fps)
    end_frame = frame_count if end_time is None else int(end_time * fps)

    prev_frame = None
    unique_frames = []

    for i in range(start_frame, end_frame, fps*3):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = video.read()
        if not ret:
            break

        current_time = i / fps
        print(f"Processing frame at {current_time:.2f} seconds")

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
        else:
            unique_frames.pop()
            unique_frames.append((i, frame))
            prev_frame = gray_frame

    video.release()
    return unique_frames, fps

def save_extracted_frames(output_dir, unique_frames, fps):
    for i, (frame_idx, frame) in enumerate(unique_frames):
        timestamp = frame_idx / fps
        file_name = f"{output_dir}/ppt_frame_{frame_idx}_time_{timestamp:.2f}.png"
        cv2.imwrite(file_name, frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract PPT frames from a video")
    parser.add_argument("video_file", help="Path to the video file")
    parser.add_argument("output_dir", help="Path to the output directory")
    parser.add_argument("--start_time", type=float, default=0, help="Start time in seconds (default: 0)")
    parser.add_argument("--end_time", type=float, default=None, help="End time in seconds (default: None)")

    args = parser.parse_args()

    video = cv2.VideoCapture(args.video_file)
    total_duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
    video.release()

    segment_duration = 20 * 60  # 20 minutes
    start_time = 0
    end_time = segment_duration

    while start_time < total_duration:
        print(f"Processing segment from {start_time} to {end_time} seconds")
        unique_frames, fps = extract_ppt_frames(args.video_file, start_time=start_time, end_time=end_time)
        save_extracted_frames(args.output_dir, unique_frames, fps)

        start_time += segment_duration
        end_time += segment_duration
        end_time = min(end_time, total_duration)

        
