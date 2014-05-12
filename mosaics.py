import matplotlib.pyplot as plt
import numpy as np

from skimage import data, io, filter
from PIL import Image
from PIL import ImageFilter

import sys
import glob,os
import math

import colors as colors
from average_colors import average_colors as average_colors

io.use_plugin('pil')

def sample_skimage():
	# Process, manipulate, and save an image with skimage.
	image = data.coins()
	edges = filter.sobel(image)
	io.imshow(image)
	io.show()
	io.imsave("edges.png", edges) 

def euclidean_distance(a, b):
	sum = 0
	for i in range(len(a)):
		sum += (a[i] - b[i]) ** 2
	return math.sqrt(sum)

def most_similar_image(im):
	img_color = colors.average_color(im)
	min_dist = float("inf")
	img = None
	for i in range(len(average_colors)):
		col = average_colors[i]
		dist = euclidean_distance(col, img_color)
		if dist < min_dist:
			min_dist = dist
			img = "images/im" + str(i+1) + ".jpg"
	return Image.open(img).convert('RGB')

##### Process, manipulate, and save images by stitching with image. ######
def make_picture(pic):
	im = Image.open(pic).convert('RGB')
	x, y = im.size
	# box tuples are left, upper, right, lower. 0,0 is the upper left corner.
	increments = max(x / 100, 50)
	boxes = []
	x_inc = x / increments;
	y_inc = y / increments;
	for i in range(increments + 1):
		for j in range(increments + 1):
			x_start = i * x_inc
			y_start = j * y_inc
			b = [x_start, y_start, x_start + x_inc, y_start + y_inc]
			boxes.append(b)
	
	for b in boxes:
		image = most_similar_image(im.crop(b))
		image = image.resize((b[2]-b[0], b[3]-b[1]))
		im.paste(image, b)
	im = im.crop((0, 0, x - (x % increments), y - (y % increments))) 
	im.show()
	im.save('image.jpg')
	#colors = im.getcolors()#(x * y)
	#print sorted(colors)

make_picture("profile_picture.png")
