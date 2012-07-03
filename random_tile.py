"""Example of how to use the Python Imaging Library"""
import os
import optparse

from PIL import Image

from image_transforms import tileify

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
            new_image_data = tileify(image_data, num_tiles, max_shift)
            safe_save(full_filename, new_image_data)
        except IOError:
            print "Can not modify " + full_filename
    else:
        print 'Must enter photo in this directory'


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
