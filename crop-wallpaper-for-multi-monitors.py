#!/usr/bin/env python
import argparse
import os
from collections import namedtuple

from PIL import Image

Viewport = namedtuple('Viewport', ['name', 'padding', 'width', 'height'])
Dimension = namedtuple('Dimension', ['width', 'height'])


def main():
    args = parse_args()
    min_resolution = get_viewports_required_min_resolution(args.viewports)

    print('Loading image... {}'.format(args.source_image_path))
    image = Image.open(args.source_image_path)

    if image.size[0] < min_resolution.width or image.size[1] < min_resolution.height:
        image = up_scale_w_aspect_ratio(image, min_resolution)

    x = 0
    y = (image.height - min_resolution.height) / 2
    remaining_viewport_width = min_resolution.width

    for viewport in args.viewports:
        if viewport.padding == 'auto':
            x += (image.width - x - remaining_viewport_width) / 2
        else:
            x += viewport.padding

        save_a_crop(
            '{}{}'.format(args.destination_image_path, viewport.name),
            image,
            left=x,
            top=y,
            width=viewport.width,
            height=viewport.height
        )

        x += viewport.width
        remaining_viewport_width -= viewport.width


def parse_args():
    parser = argparse.ArgumentParser(description='Slicing image', formatter_class=WideHelpFormatter)

    parser.add_argument(
        'source_image_path', metavar='PATH', type=str,
        help='Path of the source image.'
    )
    parser.add_argument(
        'destination_image_path', metavar='PREFIX', type=str,
        help='Path of the destination JPEG image.'
    )
    parser.add_argument(
        'viewports', metavar='NAME_PAD_W_H', nargs='+', type=parse_viewport,
        help='Name, left-pad size and viewport resolution (with, height). All sub-parameters should be separated by '
             'colon. You can specify multiple crops where the image will processing from left to right. The padding '
             'size can a positive integer or \'auto\' for crop the center of the remaining image.'
    )

    parser.epilog = """
EXAMPLES:
  For cropping the center of the image:
    %(prog)s /foo/bar/source.jpg /foo/bar/source_crop center,auto,1920,1080

  For cropping the left and right parts into separated image:
    %(prog)s /foo/bar/source.jpg /foo/bar/source_crop left,0,1920,1080 right,0,1920,1080

  For cropping the left and right parts with sip a gap for e.g. emulate the distance of the monitors:
    %(prog)s /foo/bar/source.jpg /foo/bar/source_crop left,0,1920,1080 right,200,1920,1080
"""

    args = parser.parse_args()

    return args


class WideHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, prog, *args, **kwargs):
        indent_increment = 2
        max_help_position = 40
        width = int(os.getenv('COLUMNS', 120)) - 2

        super(WideHelpFormatter, self).__init__(prog, indent_increment, max_help_position, width)


def parse_viewport(arg):
    """
    :rtype: Viewport
    """

    try:
        name, padding, width, height = arg.split(',')
        if padding != 'auto':
            padding = int(padding)
        return Viewport(name, padding, parse_dimension(width), parse_dimension(height))
    except ValueError:
        raise argparse.ArgumentTypeError(
            '{!r} can\'t be parsed as viewport parameters; '
            'required form: name(str),pad(\'auto\'|int),width(int),height(int)'.format(arg)
        )


def parse_dimension(arg):
    """
    :rtype: int
    """

    value_error = argparse.ArgumentTypeError('{!r} is bad dimension; should be greater than 0 integer'.format(arg))

    try:
        value = int(arg)
    except ValueError:
        raise value_error

    if value < 1:
        raise value_error

    return value


def get_viewports_required_min_resolution(viewports):
    """
    :type viewports: list[Viewport]
    :rtype Dimension
    """

    height = 0
    width = 0

    for viewport in viewports:
        height = max(height, viewport.height)

        width += viewport.width
        if viewport.padding != 'auto':
            width += viewport.padding

    return Dimension(width, height)


def up_scale_w_aspect_ratio(image, min_size):
    """
    :param image: Image
    :type min_size: Dimension
    """

    ratio = max(float(min_size.width) / image.width, float(min_size.height) / image.height)

    new_dimension = Dimension(
        width=max(
            int(round(image.width * ratio)),
            min_size.width
        ),
        height=max(
            int(round(image.height * ratio)),
            min_size.height
        )
    )

    print('Up-scaling image... {orig} >> {new} [x{ratio}]'.format(
        orig=format_dimension(*image.size),
        new=format_dimension(*new_dimension),
        ratio=ratio
    ))

    return image.resize(new_dimension, Image.ANTIALIAS)


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

    print('Cropping image... {orig} >> {new} @ {path}'.format(
        orig=format_dimension(orig_width, orig_height),
        new=format_view(left, top, width, height),
        path=destination_path
    ))
    cropped_image.save(destination_path, format='jpeg')


def format_dimension(width, height):
    return '[ {width:d}x{height:d} ]'.format(
        width=width, height=height
    )


def format_view(left, top, width, height):
    return '[ {left:d}x{top:d}, {width:d}x{height:d} ]'.format(
        left=left, top=top, width=width, height=height
    )


if __name__ == '__main__':
    main()
