#
#
# Basic interface to the icons in the current directory.
#
#

from PIL import Image, ImageTk
import os

ICONS = {}
for icon in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    fname, ext = os.path.splitext(icon)

    if ext not in [".png", ".PNG", ".jpg", ".JPG", ".gif", ".GIF"]:
        #Only load supported images
        continue

    timage = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     icon))
    ICONS[fname] = ImageTk.PhotoImage(timage)


