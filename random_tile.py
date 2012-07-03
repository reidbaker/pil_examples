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
    parser.add_option(
        "--max-shift",
        "-m",
        dest='max_shift',
        type="int",
        help='The max amount a block can randomly shift'
    )
    parser.add_option(
        "--num-tiles",
        "-n",
        dest='num_tiles',
        type="int",
        help='The number of tiles to break an image into'
    )
    (opts, args) = parser.parse_args()

    # Give user feedback if they forget an option and exit
    mandatory_options = ['filename']
    for option in mandatory_options:
        if not opts.__dict__[option]:
            print "Mandatory option is missing\n"
            parser.print_help()
            exit(-1)

    max_shift = opts.max_shift
    if max_shift == None:
        max_shift = 50

    num_tiles = opts.num_tiles
    if num_tiles == None:
        num_tiles = 20

    full_filename =  opts.filename
    if full_filename != None:
        try:
            image_data = Image.open(full_filename)
            new_image_data = tileify(image_data, 20, max_shift)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'

def tileify(image_data, num_blocks, max_shift):
    width = image_data.size[0]
    height = image_data.size[1]
    row_block_size = round(height / num_blocks)
    col_block_size = round(width / num_blocks)
    negitive_image = ImageOps.invert(image_data)
    pixels = numpy.array(image_data)
    for row in xrange(num_blocks):
        inner_row_val = int(row_block_size * row)
        outer_row_val = int(row_block_size * row + row_block_size)
        for col in xrange(num_blocks):
            inner_col_val = int(col_block_size * col)
            outer_col_val = int(col_block_size * col + col_block_size)
            block = pixels[
                inner_row_val:outer_row_val,
                inner_col_val:outer_col_val
            ]
            x_offset = numpy.random.random_integers(-max_shift, max_shift)
            y_offset = numpy.random.random_integers(-max_shift, max_shift)
            location = (
                inner_col_val + y_offset,
                inner_row_val + x_offset
            )
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
