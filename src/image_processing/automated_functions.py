
from skimage import io
import matplotlib.pyplot as plt
import os
import cv2
from src.file_handler.file_handler import ensure_create_dir
from src.image_processing.skeletonize import skeletonize_image
from src.file_handler.file_handler import get_filename_without_extention
from src.image_processing.common_functions.common_functions import get_dir
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.gabor_filter import gabor_filter


def gabor_filter_automated(directory: str = None):
    """
    Applies the gabor filter with given paramters to
    all images with the extension png in the selected directory and
    saves the results.

    Args:
       directory (str, optional): the path to the directory that should
       be processed.

    Returns:
        list: The list of filtered images.
    """
    save = False
    if directory is None:
        directory = get_dir()
        save = True

    results = []

    for entry in os.scandir(directory):
        if (entry.path.endswith("_skel.png")):
            path2 = get_filename_without_extention(entry.path)
            path = entry.path
            result = gabor_filter(get_image(path))
            if save:
                cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)
            results.append(result)

    return results


def skeletonize_automated(directory: str = None):
    """
    Skeletonizes all images with the extension png in the selected directory and
    saves the results.

    Args:
       directory (str, optional): the path to the directory that should
       be processed.

    Returns:
        list: The list of skeletonized images.
    """
    save = False
    if directory is None:
        directory = get_dir()
        save = True

    results = []

    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = get_filename_without_extention(entry.path)
            path = entry.path
            img = skeletonize_image(io.imread(path))
            if save:
                plt.imsave(directory + '/' + path2 + '_skel.png', img, cmap=plt.cm.gray)
            results.append(img)

    return results


def process_dataset(directory: str = None):
    """
    Applies skeletonization and gabor filter to the given dataset
    with the standard structure.

    Args:
       directory (str): the path to the directory that should
       be processed.
    """
    if directory is None:
        directory = get_dir()

    for dir in os.listdir(directory):
        if not dir.startswith('.'):
            dir2 = directory + '/' + dir + '/'
            dir3 = directory + '/' + dir + '/skel/'
            ensure_create_dir(dir3)
            for file in os.listdir(dir2):
                if file.endswith('.png'):
                    filename = get_filename_without_extention(file)
                    skeleton = skeletonize_image(path=dir2 + file)
                    cv2.imwrite(dir3 + filename + '_skel.png', skeleton)
                    gabor = gabor_filter(path=dir3 + filename + '_skel.png')
                    cv2.imwrite(dir3 + filename + '_skel_control_points.png', gabor)