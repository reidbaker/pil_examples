"""Example of how to use the Python Imaging Library"""
import os
import optparse

import numpy
from PIL import Image
from PIL import ImageOps

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
            new_image_data = tileify(image_data, 10)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def tileify(image_data, num_blocks):
    width = image_data.size[0]
    height = image_data.size[1]
    block_size = round(height / num_blocks)
    negitive_image = ImageOps.invert(image_data)
    pixels = numpy.array(image_data)
    for i in xrange(num_blocks):
        inner_block_edge = int(block_size * i)
        outer_block_edge = int(block_size * i + block_size)
        block = pixels[inner_block_edge:outer_block_edge, inner_block_edge:outer_block_edge]
        x_offset = numpy.random.random_integers(1,10)
        y_offset = numpy.random.random_integers(1,10)
        location = (
            inner_block_edge + x_offset,
            inner_block_edge + y_offset
        )
        print location
        negitive_image.paste(Image.fromarray(block), location)
    return negitive_image

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
