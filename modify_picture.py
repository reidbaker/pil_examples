import os
import sys
from PIL import Image

def main():
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
    print 'rotating'
    return image_data

def safe_save(full_filename, new_image_data):
    filename, extention = os.path.splitext(full_filename)
    new_image_data.save(filename + '_modified' + extention)

if __name__ == "__main__":
    main()
