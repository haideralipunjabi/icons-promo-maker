# icons-promo-maker
# Author: Haider Ali Punjabi
# Mail: developer@hackesta.org

import math
import os
from PIL import Image, ImageDraw, ImageFont

ICONS_FOLDER = "icons/"                         # Directory containing icons
ASSETS_FOLDER = "assets/"                       # Directory containing assets
SUPPORTED_TYPES = ["png"]                       # Supported filetypes for icons
GITHUB_URL = "hackesta/atom-icons"              # Github URL to add to image
IMAGE_CONFIG = {
    "name": "promo.png",                        # Name of Image Generated
    "mode": "RGB",                              # Image Mode used
    "title": "Icons based on Coding Train",     # Title to be used in Image
    "github_mark": "dark",                      # light/dark Github Icon to be used, opposite shade to background
    "dimensions": (512,512),                  # Dimensions of Image
    "background": "#F5F5F5",                    # Background of Image
    "text_color": "#000000",                    # Text color used in image
    "text_font": "OpenSans-Light.ttf",          # Font to use in image
    "text_size": 24,                            # Text size to be used in image, best: 5% of Image Height
    "spacing": 10                               # Spacing between icons, texts, etc
}


# factor_int: divide a number into rows and cols
# Source: https://stackoverflow.com/a/39248503/4698800
# TODO: Improve function to return multiple rows for primes, e.g, 7,11,13 all return 1 row
def factor_int(n):
    nsqrt = math.ceil(math.sqrt(n))
    solution = False
    val = nsqrt
    while not solution:
        val2 = int(n/val)
        if val2 * val == float(n):
            solution = True
        else:
            val -= 1
    return val, val2


def main():
    if not os.path.exists(ICONS_FOLDER):
        print(ICONS_FOLDER + " NOT FOUND")
        return
    if not os.path.exists(ASSETS_FOLDER):
        print(ASSETS_FOLDER + " NOT FOUND")
        return
    # Create base image
    image = Image.new(IMAGE_CONFIG['mode'], IMAGE_CONFIG['dimensions'], IMAGE_CONFIG['background'])
    width, height = IMAGE_CONFIG['dimensions']
    draw = ImageDraw.Draw(image)
    # Draw title and github url
    font = ImageFont.truetype(ASSETS_FOLDER+IMAGE_CONFIG['text_font'], IMAGE_CONFIG['text_size'])
    # Drawing title, horizontally middle aligned, vertically at 10% of height
    w, h = draw.textsize(IMAGE_CONFIG['title'], font)
    draw.text(((width-w)/2, height/10), IMAGE_CONFIG['title'], fill=IMAGE_CONFIG['text_color'], font=font)
    # Drawing title, horizontally middle aligned, vertically at 90% of height
    w, h = draw.textsize(GITHUB_URL, font)
    draw.text(((width-w)/2, (9*height)/10), GITHUB_URL, fill=IMAGE_CONFIG['text_color'], font=font)
    github = Image.open(ASSETS_FOLDER + "github_" + IMAGE_CONFIG['github_mark'] + ".png")
    github = github.resize((h,h), Image.ANTIALIAS)
    image.paste(github, ((width-w)//2 - h - IMAGE_CONFIG['spacing'], (9*height)//10), mask=github)
    # Add Icons
    icon_count = 0
    for icon in os.listdir(ICONS_FOLDER):
        if SUPPORTED_TYPES.__contains__(icon.split('.')[1]):
            icon_count += 1
    if icon_count == 0:
        print("No Icons Found")
        return
    rows, cols = factor_int(icon_count)
    # Defining borders for icon placement
    left = 0
    right = width
    # Top is at 10% height + height of title + defined spacing * 2
    top = height//10 + draw.textsize(IMAGE_CONFIG['title'],font)[1] + IMAGE_CONFIG['spacing']*2
    # Bottom is at 90% height - defined spacing * 2
    bottom = (9*height)//10 - IMAGE_CONFIG['spacing']*2
    # draw.line([left,top,right,top], fill="#000000",width=1)
    # draw.line([left,bottom,right,bottom], fill="#000000", width=1)
    for i in range(0,rows):
        for j in range(0, cols):
            icon = Image.open(ICONS_FOLDER + os.listdir(ICONS_FOLDER)[i*cols + j])
            # xsize: max width of each icon possible
            xsize = ((right-left) - (IMAGE_CONFIG['spacing'] * cols)) // cols
            # ysize: max height of each icon possible
            ysize = ((bottom-top) - (IMAGE_CONFIG['spacing'] *rows)) // rows
            # use the least of xsize & ysize
            size = xsize if (xsize <= ysize) else ysize
            icon = icon.resize((size,size), Image.ANTIALIAS)
            # The below used formula, although not beautiful, results in a symmetric and beautiful output
            # Aligns all the icons horizontally and vertically center w.r.t the defined borders
            image.paste(icon,
                        (left + ((right - left) - (IMAGE_CONFIG['spacing']*cols) - (size * cols))//2 + (j * size) + (IMAGE_CONFIG['spacing'] *j),
                         top + ((bottom - top) - (IMAGE_CONFIG['spacing']*rows) - (size * rows))//2 + (i * size) + (IMAGE_CONFIG['spacing']*i)),
                        mask=icon)
    image.save(IMAGE_CONFIG['name'])


main()

