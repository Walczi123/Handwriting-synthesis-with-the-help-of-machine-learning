from skimage.morphology import skeletonize
from skimage import filters
from skimage import io
import matplotlib.pyplot as plt
from skimage.util import invert
import cv2
import numpy as np
from src.image_processing.common_functions.common_functions import get_dir_and_file


def skeletonize_image(image):
    """
    Generate skeleton from image.

    Args:
        image (image): Input image.

    Returns:
        image: Output image with skeleton
    """
    image = invert(image)
    image = image > filters.threshold_otsu(image)

    skeleton = skeletonize(image)
    skeleton = invert(skeleton)
    return skeleton


def skeletonize_function():
    """
    Sekeletonize the selected image, shows the result and saves it.
    Args:
       None
    """
    directory, path2, path = get_dir_and_file()

    image2 = io.imread(path)
    skeleton = skeletonize_image(image2)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                             sharex=True, sharey=True)

    ax = axes.ravel()

    ax[0].imshow(image2, cmap=plt.cm.gray)
    ax[0].axis('off')
    ax[0].set_title('original', fontsize=20)

    ax[1].imshow(skeleton, cmap=plt.cm.gray)
    ax[1].axis('off')
    ax[1].set_title('skeleton', fontsize=20)

    fig.tight_layout()
    plt.imsave('text_skel.png', skeleton, cmap=plt.cm.gray)
    image4 = cv2.imread('text_skel.png')
    image4 = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)
    for ix, iy in np.ndindex(image4.shape):
        if(image4[ix, iy] != 255):
            image4[ix, iy] = 0
    # _, img = cv2.threshold(image4, 2, 255, cv2.THRESH_BINARY)
    plt.imsave(directory + '/' + path2 + '_skel.png', image4, cmap=plt.cm.gray)
    plt.show()


if __name__ == '__main__':
    skeletonize_function()