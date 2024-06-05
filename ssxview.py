#!/usr/bin/env python
#
# View SAM SSX screen image
#
# https://github.com/simonowen/ssxview/

import sys
import argparse
from PIL import Image     # requires Pillow ("python -m pip install pillow")

def rgb_from_index(i):
    """Map SAM palette index to RGB tuple"""
    # Note: this uses the same linear intensities as SimCoupe.
    intensities = [0x00, 0x24, 0x49, 0x6d, 0x92, 0xb6, 0xdb, 0xff]
    red = intensities[(i & 0x02) | ((i & 0x20) >> 3) | ((i & 0x08) >> 3)]
    green = intensities[((i & 0x04) >> 1) | ((i & 0x40) >> 4) | ((i & 0x08) >> 3)]
    blue = intensities[((i & 0x01) << 1) | ((i & 0x10) >> 2) | ((i & 0x08) >> 3)]
    return (red, green, blue)

def sam_palette():
    """Create a list of RGB values for the SAM palette of 128 colours"""
    return [rgb_from_index(i) for i in range(128)]

def mode1_colour(img_data, x, y):
    """Return CLUT index of mode 1 display at x,y"""
    data_offset = ((y & 0xc0) << 5) + ((y & 0x38) << 2) + ((y & 0x07) << 8) + ((x & 0xf8) >> 3)
    attr_offset = 0x1800 + ((y & 0xf8) << 2) + ((x & 0xf8) >> 3)
    data_mask = 1 << (7 - (x & 0x07))
    bright = 8 if img_data[attr_offset] & 0x40 else 0
    return bright + ((img_data[attr_offset] >> (0 if (img_data[data_offset] & data_mask) else 3)) & 7)

def mode2_colour(img_data, x, y):
    """Return CLUT index of mode 2 display at x,y"""
    data_offset = (y << 5) + ((x & 0xf8) >> 3)
    attr_offset = data_offset + 0x1800
    data_mask = 1 << (7 - (x & 0x07))
    bright = 8 if img_data[attr_offset] & 0x40 else 0
    return bright + ((img_data[attr_offset] >> (0 if (img_data[data_offset] & data_mask) else 3)) & 7)

def linear_colours(img_data, bpp):
    """Convert linear display data to CLUT indices"""
    return [(n >> (bpp * i)) & ((1 << bpp) - 1)
        for n in img_data for i in reversed(range(8 // bpp))]

def main(args):
    """Main program"""
    with open(args.ssxfile, 'rb') as f:
        data = f.read()
    size = len(data)

    palette = sam_palette()
    clut = data[-16:]

    if size == 512*192:
        img = Image.frombytes('P', (512,192), data)
        clut = range(128)
    elif size == 32*192+32*24+16:
        colours = [mode1_colour(data[:-16], x, y) for y in range(192) for x in range(256)]
        img = Image.frombytes('P', (256,192), bytes(colours))
    elif size == 32*192+32*192+16:
        colours = [mode2_colour(data[:-16], x, y) for y in range(192) for x in range(256)]
        img = Image.frombytes('P', (256,192), bytes(colours))
    elif size == 128*192+4:
        colours = linear_colours(data[:128*192], 2)
        img = Image.frombytes('P', (512,192), bytes(colours))
        clut = data[-4:]
    elif size == 128*192+16:
        colours = linear_colours(data[:128*192], 4)
        img = Image.frombytes('P', (256,192), bytes(colours))
    else:
        sys.exit(f"Invalid SSX file size ({size} bytes)")

    img.putpalette([c for i in clut for c in palette[i]])
    img = img.resize((512,384), Image.NEAREST)
    img = img.convert('RGB')
    img.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View SAM SSX screen image")
    parser.add_argument('ssxfile')
    main(parser.parse_args())
