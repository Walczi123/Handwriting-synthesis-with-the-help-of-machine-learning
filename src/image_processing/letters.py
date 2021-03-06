""" Extraction letters from images """
import os
from PIL import Image
from src.image_processing.resize import crop_image


def check_char(path, char: str):
    """
    Function for replacing problematic characters with their string description for folder creation
    Args:
        path (str): Parent directory of the new folder.
        char (str): Character to check and replace.
    Returns:
        (str): Complete path for the new folder.
    """
    if char == ':':
        return path + '/colon/'
    elif char == '.':
        return path + '/dot/'
    elif char == '?':
        return path + '/question/'
    elif char == '*':
        return path + '/asterisk/'
    elif char == '"':
        return path + '/quote/'
    elif char == '~':
        return path + '/tilde/'
    else:
        if char.islower():
            return path + '/' + char + '2/'
        else:
            return path + '/' + char + '/'


def extract(directory, path=None):
    if path is None:
        path = directory
    letters = path + '/letters_dataset'
    if not os.path.exists(letters):
        os.mkdir(letters)
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".png":
            image = directory + '/' + filename

            im = Image.open(image)
            width, height = im.size

            command = 'tesseract ' + image + ' ' + \
                image[:-4] + ' -l engnew makebox quiet'
            os.system(command)

            boxfilename = image[:-3] + 'box'
            file1 = open(boxfilename, "r")
            lines = file1.readlines()
            for line in lines:
                words = line.split()
                left = int(words[1])
                bottom = height - int(words[2])
                right = int(words[3])
                top = height - int(words[4])
                im1 = im.crop((left, top, right, bottom))
                letterdir = check_char(letters, words[0])
                if os.path.exists(letterdir):
                    count = len([sample for sample in os.listdir(letterdir)])
                else:
                    os.mkdir(letterdir)
                    count = 0
                im1.save(letterdir + str(count) + '.png')
                crop_image(letterdir + str(count) + '.png',
                           letterdir + str(count) + '.png')

            file1.close()
    return letters
