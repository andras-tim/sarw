#!/usr/bin/env python

import sys
from PIL import Image


def main(*args):
    source_image_path, destination_jpg_path_prefix = args

    print('Loading image... {}'.format(source_image_path))
    image = Image.open(source_image_path)
    new_width = image.size[0] / 2

    save_a_crop('{}_a-left'.format(destination_jpg_path_prefix), image, width=new_width)
    save_a_crop('{}_b-right'.format(destination_jpg_path_prefix), image, left=new_width)
    save_a_crop('{}_c-center'.format(destination_jpg_path_prefix), image, left=new_width / 2, width=new_width)


def save_a_crop(destination_path, image, left=0, top=0, width=None, height=None):
    orig_width, orig_height = image.size

    if left is None:
        left = 0
    if top is None:
        top = 0
    if width is None:
        width = orig_width - left
    if height is None:
        height = orig_height - top

    cropped_image = image.crop((left, top, left + width, top + height))

    destination_path = '{}.jpg'.format(destination_path)
    print('Cropping image... {orig} >> {new} @ {path}'.format(
        orig=get_dimension(0, 0, orig_width, orig_height),
        new=get_dimension(left, top, width, height),
        path=destination_path
    ))
    cropped_image.save(destination_path, format='jpeg')


def get_dimension(left, top, width, height):
    return '[ {left:d}x{top:d}, {width:d}x{height:d} ]'.format(
        left=left, top=top, width=width, height=height
    )


if __name__ == '__main__':
    main(*sys.argv[1:])
