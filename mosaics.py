from PIL import Image
from PIL import ImageFilter

import sys
import glob,os
import math
import random

import colors as colors
from average_colors import rgb_average_colors as average_colors
from closest_images import get_closest_image

############ METHODS FOR FINDING MOST SIMILAR IMAGES #######
def euclidean_distance(a, b):
	sum = 0
	for i in range(len(a)):
		sum += (a[i] - b[i]) ** 2
	return math.sqrt(sum)

def most_similar_image(im):
	img_color = colors.average_color(im)
	min_dist = float("inf")
	img_index = None
	for i in range(len(average_colors)):
		col = average_colors[i]
		dist = euclidean_distance(col, img_color)
		if dist < min_dist:
			min_dist = dist
			img_index = i+1
	img = "images/im" + str(img_index) + ".jpg"
	return Image.open(img).convert('RGB')

############ MAKE IMAGES ############

def make_picture_no_dither(pic, size, magnify=False):
	im = Image.open(pic).convert('RGB')
	x, y = im.size
	if x < 50 or y < 50:
		print "ERROR: Image is too small to render photomosaic."
		return
	if magnify:
		im = im.resize((x * 2, y * 2))
		x, y = im.size
	
	# Size of the tiles in each direction
	x_inc = size
	y_inc = size

	# Number of tiles in each direction
	x_len = x / x_inc + 1
	y_len = y / y_inc + 1

	boxes = []	
	for j in range(y_len):
		for i in range(x_len):

			x_start = i * x_inc
			y_start = j * y_inc
			b = [x_start, y_start, x_start + x_inc, y_start + y_inc]
			boxes.append(b)

	for b in boxes:
		image = most_similar_image(im.crop(b))
		im_x, im_y = image.size
		if im_x >= im_y:
			image = image.crop((im_x / 2 - im_y / 2, 0, im_x / 2 + im_y / 2, im_y))
		else:
			image = image.crop((0, im_y/2 - im_x / 2, im_x, im_y/2 + im_x / 2))
		image = image.resize((b[2]-b[0], b[3]-b[1]))
		im.paste(image, b)
	im = im.crop((0, 0, x - (x % x_inc), y - (y % y_inc))) 
	im.save('image.jpg')
	im.show()

def make_picture(pic, size, magnify=False):
	im = Image.open(pic).convert('RGB')
	x, y = im.size
	if magnify:
		im = im.resize((x * 2, y * 2))
		x, y = im.size
	if x < 50 or y < 50:
		print "ERROR: Image is too small to render photomosaic."
		return	
	
	# Size of the tiles in each direction
	x_inc = size
	y_inc = size

	# Number of tiles in each direction
	x_len = x / x_inc + 1
	y_len = y / y_inc + 1

	images = [None] * len(average_colors)

	# Pixel representation of the image
	small = im.resize((x_len, y_len), Image.ANTIALIAS)
	data = small.getdata()
	pixels = [[None]*x_len for i in range(y_len)]
	for j in range(y_len):
		for i in range(x_len):
			pixels[j][i] = list(data[j*x_len+i])

	# Dithering and image selection
	for j in range(y_len):
		for i in range(x_len):
			if j & 1:
				i = x_len - i - 1

			x_start = i * x_inc
			y_start = j * y_inc
			b = [x_start, y_start, x_start + x_inc, y_start + y_inc]

			pixel = pixels[j][i]
			index = get_closest_image(map(lambda n: int(n)+random.randint(-20,20), pixel))

			error = [pixel[k] - average_colors[index][k] for k in range(3)]
			
			d = +1 if j & 1 else -1

			weight = 0
			if i+d >= 0 and i+d < x_len:
				weight += 7
				if j+1 < y_len:
					weight += 1
			if j+1 < y_len:
				weight += 5
				if i-d >= 0 and i-d < x_len:
					weight += 3

			if i+d >= 0 and i+d < x_len:
				for k in range(3): pixels[j][i+d][k] += error[k]*7.0/weight
				if j+1 < y_len:
					for k in range(3): pixels[j+1][i+d][k] += error[k]*1.0/weight
			if j+1 < y_len:
				for k in range(3): pixels[j+1][i][k] += error[k]*5.0/weight
				if i-d >= 0 and i-d < x_len:
					for k in range(3): pixels[j+1][i-d][k] += error[k]*3.0/weight

			if images[index] is None:
				folder = "small_images"
				if x_inc <= 50 and y_inc <= 50:
					folder = "thumbnails"

				image = Image.open(folder + "/im"+str(index+1)+".jpg").convert('RGB')
				
				if not (x_inc == 50 and y_inc == 50):
					image = image.resize((b[2]-b[0], b[3]-b[1]))

				images[index] = image
			else:
				image = images[index]
			im.paste(image, b)
	im = im.crop((0, 0, x - (x % x_inc), y - (y % y_inc))) 
	im.save('image.jpg')
	im.show()

make_picture("prague.jpg", 50, True)
#make_picture_no_dither("prague.jpg", 50, True)
