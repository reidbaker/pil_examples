"""Example of how to use the Python Imaging Library"""
import os
import optparse

from PIL import Image
from PIL import ImageDraw
from image_transforms import filmify_image

def main():
    """Retrieves file entered, manipulates it and saves a copy with a new name"""
    # Parse options
    parser = optparse.OptionParser()
    parser.add_option(
        "-f",
        dest="filename",
        help="Picture to modify",
        metavar="FILE"
    )
    parser.add_option(
        "-s",
        dest='custom_string',
        help='String to be placed at the top of the film'
             'Default is Kodak'
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
            new_image_data = filmify_image(image_data)
            add_text_header(new_image_data, text=opts.custom_string)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def add_text_header(image_data, text='Kodak'):
    """
    Add text to the top of the document
    Inputs
        image_data - image to have text added
        text - string to add
    """
    # TODO add string wrapping for long strings
    # TODO figure this out programatically
    text_location = (300, 1)
    # This is white
    fill_color = 255
    # This happens if -s wasn't set
    if text == None:
        text = 'Kodak'
    draw = ImageDraw.Draw(image_data)
    draw.text(text_location, text, fill=fill_color)

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
