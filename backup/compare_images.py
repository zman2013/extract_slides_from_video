import argparse
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def compare_images(image_path1, image_path2):
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # 转换为灰度图像
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # similarity = np.sum(gray_image1 == gray_image2) / gray_image1.size

    # 计算 SSIM 相似度
    similarity = ssim(gray_image1, gray_image2, full=True, multichannel=False)[0]

    return similarity, image1, image2

def display_images(image1, image2):
    combined_image = cv2.hconcat([image1, image2])
    cv2.imshow("Image Comparison", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate similarity between two images")
    parser.add_argument("image_path1", help="Path to the first image")
    parser.add_argument("image_path2", help="Path to the second image")

    args = parser.parse_args()

    similarity, image1, image2 = compare_images(args.image_path1, args.image_path2)
    print(f"Similarity between '{args.image_path1}' and '{args.image_path2}': {similarity:.4f}")

    display_images(image1, image2)
