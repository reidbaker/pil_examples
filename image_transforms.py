"""Transformations on images"""
import numpy

import Image
from PIL import ImageOps

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
