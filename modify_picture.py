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
    film_size = (400, 300)
    border_size = 20
    film_hole_size = (5,10)
    # Center the strip in the border space
    strip_upper_offset = int(round((border_size - film_hole_size[1])/2))
    strip_lower_offset = film_size[1] + border_size + strip_upper_offset

    filmed_image = modify_photo(image_data, film_size)
    filmed_image = ImageOps.expand(filmed_image, border=border_size, fill='black')

    # Crop to cut half of border from right and left of image
    crop_box = (
        int(round(border_size/2)),
        0,
        film_size[0] + int(round(border_size * 1.5)),
        film_size[1] + border_size * 2
    )

    filmed_image = filmed_image.crop(crop_box)
    place_film_strip(filmed_image, strip_upper_offset, strip_lower_offset, film_hole_size)
    return filmed_image

def place_film_strip(image_data, y_offset_upper, y_offset_lower, film_hole_size):
    """
    Create strip of film_holes at y_offest
    """
    hole_distance = 15
    for x_offest in xrange(5, image_data.size[0], hole_distance):
        place_film_hole(image_data, (x_offest, y_offset_upper), film_hole_size)
        place_film_hole(image_data, (x_offest, y_offset_lower), film_hole_size)

def place_film_hole(image_data, offset, film_hole_size):
    """
    Puts film hole at offest into the image provided
    Inputs:
        image_data - image file to have film hole pasted
        offset - 2 tuple with x and y of the top left corner of film hole
    """
    insertion_location = (
        offset[0],
        offset[1],
        offset[0] + film_hole_size[0],
        offset[1] + film_hole_size[1]
    )
    image_data.paste('white', insertion_location)

def modify_photo(image_data, film_size):
    """
    Make the image grayscale
    All manitpulations for the origional photo go here
    """
    gray_image = ImageOps.grayscale(image_data)
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
