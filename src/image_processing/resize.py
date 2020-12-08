import cv2
import numpy as np
import os
from src.file_handler.file_handler import get_filename_without_extention


def resize_image(image_path: str, width: int, height: int):
    """
    Resizes image from given path to given size by pasting it into center of white baackground of given size

    Args:
        image_path (str): Path to image
        width (int): Width in pixels
        height (int): Height in pixels

    Returns:
        (array): Resized image
    """
    resized = np.zeros([width, height, 3], dtype=np.uint8)
    resized.fill(255)

    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    yoff = round((height - h) / 2)
    xoff = round((width - w) / 2)

    resized[yoff:yoff + h, xoff:xoff + w] = image

    return resized


def combine(path_a: str, path_b: str):
    """
    Combines 2 images into 1 with images next to each other

    Args:
        path_a (str): Path to the first image
        path_b (str): Path to the second image

    Returns:
        (array): Concatenated image
    """
    im_a = cv2.imread(path_a)
    im_b = cv2.imread(path_b)

    height, width, _ = im_a.shape

    if im_a.shape[2] == 4:
        im_a = im_a[:, :, :3]

    if im_b.shape[2] == 4:
        im_b = im_b[:, :, :3]

    return np.concatenate([im_a, im_b], axis=1)


def crop_image(image_path: str, output_path: str):
    """
    Cropps the image to the smallest possible rectangle

    Args:
        image_path (str): Path to image
        output_path (str): Output path
    """
    img = cv2.imread(image_path, 0)
    points = np.column_stack(np.where(img == 0))
    cropped = img[np.min(points[:, 0]): np.max(points[:, 0]), np.min(points[:, 1]): np.max(points[:, 0])]

    cv2.imwrite(output_path, cropped)


def resize_directory(input_path: str, output_path: str):
    """
    Resizes all images in given directory to given output directory

    Args:
        input_path (str): Input directory
        output_path (str): Output directory
    """
    i = 0
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            resized = resize_image(os.path.join(path, name), 256, 256)
            cv2.imwrite(os.path.join(output_path, str(i) + '.png'), resized)
            i += 1


def resize_skeletons_directory(input_path: str, output_path: str):
    """
    Resizes all skeleton images in given directory to given output directory

    Args:
        input_path (str): Input directory
        output_path (str): Output directory
    """
    i = 0
    for dir in os.listdir(input_path):
        if not dir.startswith('.'):
            dir2 = input_path + '/' + dir + '/skel/'
            for file in os.listdir(dir2):
                if file.endswith('.png'):
                    filename = get_filename_without_extention(file)
                    if not filename.endswith('control_points'):
                        resized = resize_image(os.path.join(dir2, file), 256, 256)
                        cv2.imwrite(os.path.join(output_path, str(i) + '.png'), resized)
                        i += 1


def combine_directory(input_path_a: str, input_path_b: str, output_path: str):
    """
    Concatenates all images in given directories to given output directory

    Args:
        input_path_a (str): First input directory
        input_path_b (str): Second input directory
        output_path (str): Output directory
    """
    for path, subdirs, files in os.walk(input_path_a):
        for name in files:
            combined = combine(os.path.join(path, name), os.path.join(input_path_b, name))
            cv2.imwrite(os.path.join(output_path, name), combined)