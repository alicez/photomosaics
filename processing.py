import colors as colors
from PIL import Image
from PIL import ImageFilter

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

from average_colors import average_colors
def tuple_transform():
	tups = []
	for i in range(len(average_colors)):
		tups.append((i + 1, average_colors[i]))
	f = open('formatted_averages.py', 'w')
	f.write('formatted_averages =')
	f.write(str(tups))

from hcluster import *
from numpy import zeros
import numpy as np
from formatted_averages import formatted_averages
from scipy import spatial
import fastcluster
from average_colors import average_colors
#def cluster_distances():
#	clusters = []
#	for i in f

def cluster_images(clusternum):
	#data  = [[0.1,0.1,0.1],
   #     [0.1,0.1,0.1],
   #     [0.1,0.1,0.1],
   #     [0.2,0.2,0.2],
   #     [0.2,0.2,0.2],
   #     [0.2,0.2,0.2],
   #     [0.3,0.3,0.3],
   #     [0.3,0.3,0.3],
   #     [0.3,0.3,0.3],]
	data = average_colors
	distance = spatial.distance.pdist(data, 'euclidean')
	print distance
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

cluster_images(1000)
