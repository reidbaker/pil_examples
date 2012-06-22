"""Example of how to use the Python Imaging Library"""
import os
import sys
from PIL import Image

def main():
    """Retrives file entered, manipulates it and saves a copy with a new name"""
    full_filename =  sys.argv[1]
    if full_filename != None:
        try:
            image_data = Image.open(full_filename)
            new_image_data = rotate_image(image_data)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify" + full_filename
    else:
        print 'Must enter photo in this directory'

def rotate_image(image_data):
    """
    Rotates an image
    Inputs:
        PIL Image
    Returns:
        Modified image data
    """
    print 'rotating'
    return image_data

def safe_save(full_filename, new_image_data):
    """
    Saves image with new name
    Inputs:
        full_filename, filename to be saved including extention e.g, myfile.jpg
        new_image_data, PIL Image data to be saved
    """
    filename, extention = os.path.splitext(full_filename)
    new_image_data.save(filename + '_modified' + extention)

if __name__ == "__main__":
    main()
