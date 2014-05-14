import colors as colors
from PIL import Image
from PIL import ImageFilter

################## METHODS FOR PROCESSING AVERAGE COLOR VALUEs ######################

# Find average RGB values for all images
def process_images():
	col = []
	for i in range(25000):
		f = "images/im" + str(i + 1) + ".jpg"
		im = Image.open(f)
		im.convert('RGB')
		im = im.resize((30, 30))
		im = im.filter(ImageFilter.BLUR)
		im.convert("P", palette=Image.ADAPTIVE, colors=256)
		print str(i)
		#im.show()
		avg = colors.average_color(im)
		col.append(avg)
	averages = open('average_colors.py', 'w')
	averages.write('average_colors =')
	averages.write(str(col))

# Find average CMYK values for all images
def process_imagesCMYK():
	col = []
	for i in range(25000):
		f = "images/im" + str(i + 1) + ".jpg"
		im = Image.open(f)
		im.convert('CMYK')
		im = im.resize((30, 30))
		im = im.filter(ImageFilter.BLUR)
		im.convert("P", palette=Image.ADAPTIVE, colors=256)
		print str(i)
		#im.show()
		avg = colors.average_color(im)
		col.append(avg)

	averages = open('cmy_colors.py', 'w')
	averages.write('cmy_colors =')
	averages.write(str(col))

# Find average XYZ values for all images
from skimage import io, color
def process_imagesXYZ():
	col = []
	for i in range(25000):
		f = "images/im" + str(i + 1) + ".jpg"
		im = io.imread(f)
		lab = color.rgb2lab(im)
		im = im.resize((30, 30))
		print str(i)
		#im.show()
		# get avg color
		t = [0, 0, 0]
		for x in range(30):
			for y in range(30):
				t[0] += im[x, y, 0]
				t[1] += im[x, y, 1]
				t[2] += im[x, y, 2]

		counts = 30 * 30
		avg = [p / counts for p in t]
		col.append(avg)
	averages = open('xyz_colors.py', 'w')
	averages.write('xyz_colors =')
	averages.write(str(col))


################## METHODS FOR PREPROCESSING CLUSTERS FROM COLORAVERAGES ######################
from hcluster import *
from numpy import zeros
import numpy as np
from scipy import spatial
import fastcluster
from average_colors import rgb_average_colors as average_colors

# cluster images into clusternum clusters, using hierarchical agglomerative clustering, with
# complete linkage.
def cluster_images(clusternum):
	data = average_colors
	distance = spatial.distance.pdist(data, 'euclidean')
	linkage = fastcluster.linkage(distance, method="complete")
	clustdict = {i:[i] for i in xrange(len(linkage)+1)}
	for i in xrange(len(linkage)-clusternum+1):
		clust1 = int(linkage[i][0])
		clust2 = int(linkage[i][1])
		clustdict[max(clustdict)+1] = clustdict[clust1] + clustdict[clust2]
		del clustdict[clust1], clustdict[clust2]
	clust = open('clust' + str(clusternum) + '.py', 'w')
	clust.write("clust" + str(clusternum) + "=")
	clust.write(str(clustdict))
	# scipy.cluster.hierarchy.fclusterdata()

#################### METHODS FOR PREPROCESSING IMAGES INTO THUMBNAILS ########################

from PIL import Image
# create square images
def create_square_image():
	for i in range(25000):
		f = "images/im" + str(i + 1) + ".jpg"
		im = Image.open(f)
		im_x, im_y = im.size
		if im_x >= im_y:
			im = im.crop((im_x / 2 - im_y / 2, 0, im_x / 2 + im_y / 2, im_y))
		else:
			im = im.crop((0, im_y/2 - im_x / 2, im_x, im_y/2 + im_x / 2))
		im.save('small_images/im' + str(i + 1) + ".jpg")

# create thumbnails
def create_square_image():
	for i in range(25000):
		f = "small_images/im" + str(i + 1) + ".jpg"
		im = Image.open(f)
		im = im.resize((50, 50))	
		im.save('thumbnails/im' + str(i + 1) + ".jpg")
#create_square_image()
cluster_images(24996)
#process_imagesCMY()
#process_imagesXYZ()
