import argparse
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import re

def is_image_file(filename):
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def compare_images(image_path1, image_path2):
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # similarity = np.sum(gray_image1 == gray_image2) / gray_image1.size
    similarity = ssim(gray_image1, gray_image2, full=True, multichannel=False)[0]

    return similarity

def get_image_index(file_name):
    match = re.search(r'ppt_frame_(\d+)_time_', file_name)
    if match:
        return int(match.group(1))
    return -1

def compare_adjacent_images(folder):
    image_files = [f for f in os.listdir(folder) if is_image_file(f)]
    image_files.sort(key=lambda x: get_image_index(x))
    
    files_to_delete = []

    for i in range(len(image_files) - 1):
        image_path1 = os.path.join(folder, image_files[i])
        image_path2 = os.path.join(folder, image_files[i + 1])

        similarity = compare_images(image_path1, image_path2)
        print(f"Similarity between '{image_files[i]}' and '{image_files[i + 1]}': {similarity:.4f}")

        if similarity > 0.95:
            print(f"Marking '{image_files[i]}' for deletion due to high similarity")
            files_to_delete.append(image_path1)

        # Delete marked files
    for file_path in files_to_delete:
        print(f"Deleting '{os.path.basename(file_path)}'")
        os.remove(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare similarity between adjacent images in a folder")
    parser.add_argument("folder", help="Path to the folder containing images")

    args = parser.parse_args()
    compare_adjacent_images(args.folder)
