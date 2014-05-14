def average_color(im):
	#im = Image.open(pic).convert('RGB')
	rgb = [0, 0, 0]
	x, y = im.size
	for i in range(x):
		for j in range(y):
			r, g, b = im.getpixel((i,j))
			rgb[0] += r
			rgb[1] += g
			rgb[2] += b
	counts = x * y
	average = [x / counts for x in rgb]
	return average

from PIL import Image
import struct
import scipy
import scipy.misc
import scipy.cluster

def most_freq_color(pic):
	im = Image.open(pic).convert('RGB')
	im = im.resize((150, 150))
	ar = scipy.misc.fromimage(im)
	shape = ar.shape
	ar = ar.reshape(scipy.product(shape[:2]), shape[2])
	codes, dist = scipy.cluster.vq.kmeans(ar, 5)
	vecs, dist = scipy.cluster.vq.vq(ar, codes)
	counts, bins = scipy.histogram(vecs, len(codes))

	index_max = scipy.argmax(counts)
	peak = codes[index_max]
	colour = ''.join(chr(c) for c in peak).encode('hex')
	print "most freq is %s (#%s)" % (peak, colour)
