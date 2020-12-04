import cv2
from src.image_processing.common_functions.common_functions import get_dir_and_file
from src.image_processing.common_functions.common_functions import get_parts
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image
from src.image_processing.common_functions.common_functions import resize_and_show_images
import sys
import math
import random
import numpy as np


def add_end_points(halves: list, img2: np.ndarray, parts2: list):
    """
    Adds first and last points/pixel to the filtered set of control points.
    Args:
       halves (list): list of selected points/pixels.
       img2 (np.ndarray): image with filtered control points.
       parts2 (list): list of subparts of the initial image that
            that still contains control points.
    """
    halves.append(0)
    rand_index = random.randint(0, len(parts2[0]) - 1)
    img2[parts2[0][rand_index][0], parts2[0][rand_index][1]] = 0
    parts2[0].pop(rand_index)
    halves.append(len(parts2) - 1)
    rand_index = random.randint(0, len(parts2[len(parts2) - 1]) - 1)
    img2[parts2[len(parts2) - 1][rand_index][0],
         parts2[len(parts2) - 1][rand_index][1]] = 0
    parts2[len(parts2) - 1].pop(rand_index)


def add_point(img2: np.ndarray, tmp: list, halves: list, i: int, parts2: list, offset: int):
    """
    Adds a point to the filtered set of control points.
    Args:
       img2 (np.ndarray): image with filtered control points.
       tmp (list): Copy of the list of selected points/pixels
           into which new point should be inserted.
       halves (list): The list of selected points/pixels.
       i (int): Index of the point that should be inserted.
       parts2 (list): list of subparts of the initial image that
            that still contains control points.
       offset (int): offset in the tmp list (number of previously
       inserted points compared to the halves list)
    """
    mid = math.floor((halves[i + 1] - halves[i]) / 2)
    tmp.insert(i + 1 + offset, halves[i] + mid)
    rand_index = random.randint(
        0, len(parts2[halves[i] + mid]) - 1)
    img2[parts2[halves[i] + mid][rand_index][0],
         parts2[halves[i] + mid][rand_index][1]] = 0
    parts2[halves[i] + mid].pop(rand_index)


def filter_points(img2: np.ndarray, parts: list, n: int):
    """
    Main filtering function that saves the filtered
    points/pixels in the img2 cv2 image.
    Args:
       img2 (np.ndarray): image with filtered control points.
       parts (list): list of subparts of the initial image.
       n (int): the number of subparts in each direction.
    """
    parts2 = [part for part in parts if len(part) > 0]
    state = 2
    while(state < n):
        parts2 = [part for part in parts2 if len(part) > 0]
        halves = []
        add_end_points(halves, img2, parts2)
        while(len(halves) < n and len(halves) < len(parts2)):
            tmp = halves.copy()
            offset = 0
            for i in range(0, len(halves) - 1):
                if halves[i] == (halves[i + 1] - 1):
                    continue
                add_point(img2, tmp, halves, i, parts2, offset)
                offset += 1
                state += 1
                if(state == n):
                    break
            halves = tmp
            if(state == n):
                break


def binary_search_filter():
    """
    Creates the subparts, filters the control points, shows the
    results and saves the result.
    Args:
        None
    """
    if len(sys.argv) == 1:
        exit()
    n = int(sys.argv[1])

    directory, path2, path = get_dir_and_file()

    img = get_image(path)

    parts = []
    get_parts(img, n, parts)

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])

    img2 = prepare_blank_image(img)
    filter_points(img2, parts, n)
    resize_and_show_images(img, img2)
    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    binary_search_filter()