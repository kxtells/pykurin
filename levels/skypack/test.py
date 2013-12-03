from PIL import Image, ImageFilter

image = Image.open('1LongCloudCOL.png')
image = image.filter(ImageFilter.FIND_EDGES)
image.save('new_name.png')
