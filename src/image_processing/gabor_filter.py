import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.image_processing.common_functions.common_functions import get_dir_and_file


def nothing(x):
    """
    Does nothing. It is used as sliders handler.
    Args:
       None - x is a surrogate argument.
    """
    pass


def save(x1, x2):
    """
    Saves current result of the filtering to the final result image.
    The images are accessed as global variables.
    Args:
       None - x1 and x2 are surrogate arguments.
    """
    global result
    global cv_image
    result = np.bitwise_and(result, cv_image)


def gabor_filter():
    """
    Main function. Creates GUI for changing the filtering parmeters,
    shows and saves the result.
    Args:
       None
    """
    global result
    global cv_image
    directory, path2, path = get_dir_and_file()
    img2 = np.zeros((300, 512, 3), np.uint8)
    cv2.namedWindow('trackbar')

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = np.zeros(shape=img.shape)
    result = img_as_ubyte(result)
    result = invert(result)

    cv2.createTrackbar('theta', 'trackbar', 25, 300, nothing)
    cv2.createTrackbar('lamda', 'trackbar', 16, 300, nothing)
    cv2.createTrackbar('offset', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('n_stds', 'trackbar', 3, 300, nothing)
    cv2.createTrackbar('bandwidth', 'trackbar', 10, 300, nothing)
    cv2.createTrackbar('sigma_x', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('sigma_y', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('cval', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('cval', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('n', 'trackbar', 1, 300, nothing)
    cv2.createButton('save control points', save, [''], cv2.QT_PUSH_BUTTON)
    while(1):
        cv2.imshow('trackbar', img2)
        k = cv2.waitKey(1) & 0xFF
        if k == 97:
            break

        theta = cv2.getTrackbarPos('theta', 'trackbar') * 0.01 * np.pi
        lamda = cv2.getTrackbarPos('lamda', 'trackbar') * 0.01 * np.pi
        offset = cv2.getTrackbarPos('offset', 'trackbar') * 0.1
        bandwidth = cv2.getTrackbarPos('bandwidth', 'trackbar') * 0.1
        sigma_x = cv2.getTrackbarPos('sigma_x', 'trackbar') * 0.1
        sigma_y = cv2.getTrackbarPos('sigma_y', 'trackbar') * 0.1
        cval = cv2.getTrackbarPos('cval', 'trackbar') * 0.1
        n_stds = cv2.getTrackbarPos('n_stds', 'trackbar')
        if bandwidth == 0:
            continue
        img = cv2.imread(path)

        plt.imshow(img, cmap='gray')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if sigma_x == 0 or sigma_y == 0:
            filt_real, filt_imag = gabor(
                img, frequency=1 / lamda, theta=theta, n_stds=n_stds, offset=offset, bandwidth=bandwidth, cval=cval)
        else:
            filt_real, filt_imag = gabor(img, frequency=1 / lamda, theta=theta, n_stds=n_stds,
                                         offset=offset, bandwidth=bandwidth, sigma_x=sigma_x, sigma_y=sigma_y, cval=cval)

        cv2.imshow('Original Img.', img)
        cv_image = img_as_ubyte(filt_imag)
        cv_image = invert(cv_image)
        cv_image3 = img_as_ubyte(filt_real)
        cv_image3 = invert(cv_image3)

        size = (200, 200)
        cv_image2 = cv2.resize(cv_image, size)
        cv_image4 = cv2.resize(cv_image3, size)

        cv2.imshow('Filtered imag', cv_image2)
        cv2.imshow('Filtered real', cv_image4)

    cv2.destroyAllWindows()

    cv2.imshow('Result', result)
    cv2.waitKey()
    cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)


if __name__ == '__main__':
    gabor_filter()