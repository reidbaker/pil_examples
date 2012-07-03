"""Transformations on images"""
from numpy import random
from numpy import array
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps

def tileify(image_data, num_blocks, max_shift):
    """
    Breaks image up into rectangles and shifts them a random distance
    Areas not covered by the moved rectangles are the negative of
    the original image
    """
    width = image_data.size[0]
    height = image_data.size[1]
    row_block_size = round(height / num_blocks)
    col_block_size = round(width / num_blocks)
    negative_image = ImageOps.invert(image_data)
    pixels = array(image_data)
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
            location = calculate_random_location(
                inner_row_val,
                inner_col_val,
                max_shift
            )
            negative_image.paste(Image.fromarray(block), location)
    return negative_image

def calculate_random_location(x, y, max_shift):
    """
    Calculates random location near some starting point
    Inputs
        x - coordinate point where 0,0 is upper left corner
        y - coordinate point where 0,0 is upper left corner
        max_shift - the furthest distance from the point to shift
    """
    x_offset = random.random_integers(-max_shift, max_shift)
    y_offset = random.random_integers(-max_shift, max_shift)
    location = (
        y + y_offset,
        x + x_offset
    )
    return location

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
    film_hole_size = (8, 10)

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
    Output
        image with border
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

def place_film_strip(image_data, y_offset_upper, y_offset_lower, film_hole_size):
    """
    Create strip of film_holes at y_offset
    """
    hole_distance = 15
    left_film_buffer = 2
    for x_offset in range(left_film_buffer, image_data.size[0], hole_distance):
        place_film_hole(image_data, (x_offset, y_offset_upper), film_hole_size)
        place_film_hole(image_data, (x_offset, y_offset_lower), film_hole_size)

def place_film_hole(image_data, offset, film_hole_size):
    """
    Puts film hole at offset into the image provided
    Inputs:
        image_data - image file to have film hole pasted
        offset - 2 tuple with x and y of the top left corner of film hole
        film_hole_size - size of the rectangle to be made
    Outputs
        Original image with rectangle in location based on the offset
    """
    corner_radius = 2
    film_hole_color = 'white'
    film_hole = round_rectangle(film_hole_size, corner_radius, film_hole_color)
    image_data.paste(film_hole, offset)

def round_corner(radius, fill):
    """
    Draw a round corner
    This code came from http://nadiana.com/pil-tutorial-basic-advanced-drawing
    """
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def round_rectangle(size, radius, fill):
    """
    Draw a rounded rectangle
    This code came from http://nadiana.com/pil-tutorial-basic-advanced-drawing
    """
    width, height = size
    rectangle = Image.new('RGBA', size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0))
    # Rotate the corner and paste it
    rectangle.paste(corner.rotate(90), (0, height - radius))
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle

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
