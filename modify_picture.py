"""Example of how to use the Python Imaging Library"""
import os
import optparse
import ImageOps

from PIL import Image

def main():
    """Retrives file entered, manipulates it and saves a copy with a new name"""
    # Parse options
    parser = optparse.OptionParser()
    parser.add_option(
        "-f",
        dest="filename",
        help="Picture to modify",
        metavar="FILE"
    )
    (opts, args) = parser.parse_args()

    # Give user feedback if they forget an option and exit
    mandatory_options = ['filename']
    for option in mandatory_options:
        if not opts.__dict__[option]:
            print "Mandatory option is missing\n"
            parser.print_help()
            exit(-1)

    full_filename =  opts.filename
    if full_filename != None:
        try:
            image_data = Image.open(full_filename)
            new_image_data = image_film(image_data)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def image_film(image_data):
    """
    Makes the image look like film
    Inputs:
        PIL Image
    Returns:
        Modified image data
    """
    print 'Filming'
    filmed_image = modify_photo(image_data)
    return filmed_image

def modify_photo(image_data):
    gray_image = ImageOps.grayscale(image_data)
    film_size = (400, 200)
    # Image.ANTIALIAS is best for down sizing
    gray_image_small = gray_image.resize(film_size, Image.ANTIALIAS)
    return gray_image_small

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
