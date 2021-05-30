import argparse
from PIL import Image, ImageEnhance

from colors import color


def render(image_file, width=120, height_scale=0.55, colorize=True):
    img = Image.open(image_file)

    org_width, orig_height = img.size
    aspect_ratio = orig_height / org_width
    new_height = aspect_ratio * width * height_scale
    img = img.resize((width, int(new_height)))
    img = img.convert('RGBA')
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    pixels = img.getdata()

    def mapto(r, g, b, alpha):
        if alpha == 0.:
            return ' '
        chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ".", "/"]
        pixel = (r * 19595 + g * 38470 + b * 7471 + 0x8000) >> 16
        if colorize:
            return color(chars[pixel // 25], (r, g, b))
        else:
            return chars[pixel // 25]

    new_pixels = [mapto(r, g, b, alpha) for r, g, b, alpha in pixels]
    new_pixels_count = len(new_pixels)
    ascii_image = [''.join(new_pixels[index:index + width]) for index in range(0, new_pixels_count, width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display an image in ASCII with ANSI colors')

    parser.add_argument('path',
                       metavar='path',
                       type=str,
                       help='the path to the image file ')
    parser.add_argument('--no-color',
                       action='store_true',
                       help='no ANSI colors')
    parser.add_argument('--width',
                       action='store',
                       type=int,
                       default=120,
                       help='output width in characters (Default 120)')
    parser.add_argument('--height-scale',
                        action='store',
                        default=.55,
                        type=float,
                        help='scale ratio for height (default .55')
    args = parser.parse_args()
    print(render(
        args.path, 
        args.width, 
        height_scale=args.height_scale,
        colorize=not args.no_color))
