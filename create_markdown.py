import argparse
import os
import re
from datetime import datetime, timedelta
import cv2

from pysrt import SubRipFile
from pysrt import SubRipTime


def is_image_file(filename):
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def is_srt_file(filename):
    return filename.lower().endswith(".srt")


def get_image_timestamp(file_name):
    match = re.search(r'ppt_frame_(\d+)_time_(\d+\.\d+).png', file_name)
    if match:
        return float(match.group(2))
    return -1


def get_srt_file(folder):
    files = [f for f in os.listdir(folder) if is_srt_file(f)]
    if files:
        return os.path.join(folder, files[0])
    return None


def get_subtitles(srt_file, start_time, end_time, video_duration):
    subs = SubRipFile.open(srt_file)

    start_datetime = datetime.strptime(start_time, "%H:%M:%S,%f")
    end_datetime = datetime.strptime(end_time, "%H:%M:%S,%f")

    extended_start_datetime = max(start_datetime - timedelta(seconds=20), datetime.strptime("00:00:00,000", "%H:%M:%S,%f"))
    extended_end_datetime = min(end_datetime + timedelta(seconds=20), datetime(1900, 1, 1) + timedelta(seconds=video_duration) )

    start = SubRipTime(
        hours=start_datetime.hour,
        minutes=start_datetime.minute,
        seconds=start_datetime.second,
        milliseconds=start_datetime.microsecond // 1000,
    )
    end = SubRipTime(
        hours=end_datetime.hour,
        minutes=end_datetime.minute,
        seconds=end_datetime.second,
        milliseconds=end_datetime.microsecond // 1000,
    )

    extended_start = SubRipTime(
        hours=extended_start_datetime.hour,
        minutes=extended_start_datetime.minute,
        seconds=extended_start_datetime.second,
        milliseconds=extended_start_datetime.microsecond // 1000,
    )
    extended_end = SubRipTime(
        hours=extended_end_datetime.hour,
        minutes=extended_end_datetime.minute,
        seconds=extended_end_datetime.second,
        milliseconds=extended_end_datetime.microsecond // 1000,
    )

    subs_in_original_range = subs.slice(starts_after=start, ends_before=end)
    subs_in_extended_range = subs.slice(starts_after=extended_start, ends_before=extended_end)

    a = ' '.join([sub.text.replace('\n', ' ') for sub in subs_in_original_range])
    b = ' '.join([sub.text.replace('\n', ' ') for sub in subs_in_extended_range])

    start_index = b.find(a)
    stop_index = start_index + len(a)

    begin = b.rfind('.', 0, start_index)
    stop = b.find('.', stop_index)

    if begin == -1:
        begin = start_index
    else:
        begin += 1

    if stop == -1:
        stop = stop_index
    stop += 1

    subtitles_text = b[begin:stop]

    subtitles_text = subtitles_text.strip()
    if subtitles_text.startswith(">>"):
        subtitles_text = subtitles_text[2:]

    subtitles_text = subtitles_text.replace(">>", "\n\n")

    return subtitles_text


def get_video_duration(video_file_path):
    video = cv2.VideoCapture(video_file_path)
    total_duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
    video.release()
    return total_duration

def create_markdown(folder, video_file_path, output):
    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    image_files.sort(key=lambda x: get_image_timestamp(x))

    video_duration = get_video_duration(video_file_path)

    srt_file = get_srt_file(folder)

    if not srt_file:
        print("No SRT file found in the folder")
        return


    with open(output, "w") as output_file:
        for i in range(-1, len(image_files) - 1):
            if i > -1:
                timestamp1 = get_image_timestamp(image_files[i])
                start_time = f"{timedelta(seconds=timestamp1)}{',000' if '.' not in str(timestamp1) else ''}"
            else:
                start_time = f"{timedelta(seconds=0.0)}{',000' if '.' not in str(0.0) else ''}"

            image_path2 = os.path.join(folder, image_files[i + 1])
            timestamp2 = get_image_timestamp(image_files[i + 1])

            end_time = f"{timedelta(seconds=timestamp2)}{',000' if '.' not in str(timestamp2) else ''}"

            start_time = f"{start_time}{',000' if '.' not in {start_time} else ''}"
            end_time = f"{end_time}{',000' if '.' not in {end_time} else ''}"

            subtitles = get_subtitles(srt_file, start_time, end_time, video_duration)
        
            image_name2 = os.path.basename(image_path2)
            output_file.write(f"![{image_files[i + 1]}]({image_name2})\n\n")
            output_file.write(f"{subtitles}\n\n")

        # Add the last image
        image_path = os.path.join(folder, image_files[-1])
        output_file.write(f"![{image_files[-1]}]({image_path})\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to the folder containing image files and the srt file.")
    parser.add_argument("video", help="Path to the video file.")
    parser.add_argument("output", help="Path to the output file.")
    args = parser.parse_args()
    create_markdown(args.folder, args.video, args.output)

