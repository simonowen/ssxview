# ssxview.py

A Python script to view SAM Coupé SSX image files.

## Usage

View the contents of the `image.ssx` file:
```
python ssxview.py image.ssx
```

## Introduction

SSX files are designed to preserve SAM Coupé images in their native format. They
contain raw display memory data plus colour look-up table (CLUT) indices.

NOTE: this is currently an experimental file format.

## File Format

The stored data depends on the active display mode at the point of saving. There
are five possible formats, each with a unique file size:

- MODE 1 = 6144 data + 768 attrs + 16 CLUT = 6928 bytes.
- MODE 2 = 6144 data + 6144 attrs + 16 CLUT = 12304 bytes.
- MODE 3 = 24576 data + 4 CLUT = 24580 bytes.
- MODE 4 = 24576 data + 16 CLUT = 24592 bytes.
- RAW = 512x192 palette indices = 98304 bytes.

CLUT indices are in the range 0 to 15, except MODE 3 which uses 0 to 3. Palette
indices are in the full range of 0 to 127.

## Raster Effects

Many SAM software titles change display mode/page and CLUT entries mid-frame,
resulting in dynamic images that cannot be represented by the MODE data formats
listed above. These images must be saved in a RAW format, which instead stores
the palette colours at every screen pixel position. This format preserves all
raster-level effects, such as the SAM boot screen stripes.

SimCoupe detects whether VMPR/CLUT changes were made during the main screen area
and automatically saves in the RAW format instead of a MODE format. Currently
this does not extend to mid-frame display memory writes as SAM titles don't need
(or use) raster-level attribute changes for rainbowing effects.

## Samples

See the `samples` sub-directory for files in each of the formats detailed above.

---

Simon Owen  
https://simonowen.com
