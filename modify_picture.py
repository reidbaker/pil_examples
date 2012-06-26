"""Example of how to use the Python Imaging Library"""
import os
import optparse

from PIL import Image
from PIL import ImageDraw
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

def filmify_image(image_data):
    """
    Makes the image look like 35mm film
    Inputs:
        PIL Image
    Returns:
        Modified image data
    """
    print 'Filming'
    # Size of photo in side the film
    film_size = (400, 300)
    border_size = 30
    film_hole_size = (5, 10)

    filmed_image = modify_photo(image_data, film_size)
    filmed_image = add_film_border(filmed_image, film_size, border_size)

    # Center strip in the border space
    strip_upper_offset = int(round((border_size - film_hole_size[1])/2))
    strip_lower_offset = film_size[1] + border_size + strip_upper_offset
    # Bring strip in towards the photo
    offset = int(round(film_hole_size[1]/2))
    strip_upper_offset = strip_upper_offset + offset
    strip_lower_offset = strip_lower_offset - offset

    place_film_strip(
        filmed_image,
        strip_upper_offset,
        strip_lower_offset,
        film_hole_size
    )

    return filmed_image

def add_film_border(image_data, film_size, border_size):
    """
    Creates a black border around the image
    Inputs
        image_data - image to be manipulated
        film_size - size of the internal picture
        border_size - how wide you want the border on the top and bottom to be
    """
    image_data = ImageOps.expand(
        image_data,
        border=border_size,
        fill='black'
    )
    # Crop to cut half of border from right and left of image
    crop_box = (
        int(round(border_size/2)),
        0,
        film_size[0] + int(round(border_size * 1.5)),
        film_size[1] + border_size * 2
    )
    image_data = image_data.crop(crop_box)
    return image_data


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
    if text ==None:
        text = 'Kodak'
    draw = ImageDraw.Draw(image_data)
    draw.text(text_location, text, fill=fill_color)

def place_film_strip(image_data, y_offset_upper, y_offset_lower, film_hole_size):
    """
    Create strip of film_holes at y_offset
    """
    # TODO make rectangles rounded
    hole_distance = 15
    for x_offset in range(5, image_data.size[0], hole_distance):
        place_film_hole(image_data, (x_offset, y_offset_upper), film_hole_size)
        place_film_hole(image_data, (x_offset, y_offset_lower), film_hole_size)

def place_film_hole(image_data, offset, film_hole_size):
    """
    Puts film hole at offset into the image provided
    Inputs:
        image_data - image file to have film hole pasted
        offset - 2 tuple with x and y of the top left corner of film hole
    Outputs
        Original image with rectangle in location based on the offset
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
    Make the image grayscale and invert the colors
    All manipulations for the original photo go here
    """
    modified_image = ImageOps.grayscale(image_data)
    # Image.ANTIALIAS is best for down sizing
    modified_image = modified_image.resize(film_size, Image.ANTIALIAS)
    modified_image = ImageOps.invert(modified_image)
    modified_image = ImageOps.flip(modified_image)
    return modified_image

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
