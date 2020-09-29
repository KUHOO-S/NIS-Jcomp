# importing Image class from PIL package 
from PIL import Image 

# opening a multiband image (RGB specifically) 
im = Image.open(r"cool-cat-with-glasses-and-headphones-julio-cesar.jpg") 

# split() method 
# this will split the image in individual bands 
# and return a tuple 
im1 = Image.Image.split(im) 

# showing each band 
im.show()
im1[0].show() 
im1[1].show() 
im1[2].show() 

#how to merge
im2=Image.merge("RGB",(im1[0],im1[1],im1[2]))
im2.show()


# split the image into individual bands
source = im.split()

R, G, B = 0, 1, 2

# select regions where red is less than 100
mask = source[B].point(lambda i: i > 100 and 255)

# process the green band
out = source[G].point(lambda i: i * 10.7)

# paste the processed band back, but only where red was < 100
source[G].paste(out, None, mask)

# build a new multiband image
im3 = Image.merge(im.mode, source)
im3.show()

