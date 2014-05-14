import heapq
import json
import math
import sys
from average_colors import rgb_average_colors as average_colors

def _to_color_range(n):
	if n < 0: return 0
	if n > 255: return 255
	return n

def get_closest_image(color):
	r, g, b = color

	r = _to_color_range(r)
	g = _to_color_range(g)
	b = _to_color_range(b)

	index = _lookup_table[r][g][b]
	return index

def color_distance_sqr(a, b):
	dr = a[0]-b[0]
	dg = a[1]-b[1]
	db = a[2]-b[2]
	return dr*dr + db*db + dg*dg

def _save_lookup_table():
	global _lookup_table

	f = open('closest_image_lookup_table.json', 'w')
	f.write(json.dumps(_lookup_table))
	f.close()

def _load_lookup_table():
	global _lookup_table

	try:
		f = open('closest_image_lookup_table.json', 'r')
		_lookup_table = json.loads(f.read())
		f.close()
	except IOError:
		_lookup_table = []

_lookup_table = []
def _init_lookup_table():
	global _lookup_table

	_lookup_table = [[[-1]*256 for i in range(256)] for j in range(256)]

	heap = []
	for i, color in enumerate(average_colors):
		heapq.heappush(heap, (0, i, color))
		r, g, b = color

	done = 0
	while heap:
		distance_sqr, origin, color = heapq.heappop(heap)
		r, g, b = color
		if _lookup_table[r][g][b] != -1:
			continue
		_lookup_table[r][g][b] = origin
		done += 1
		_add_neighbors_to_heap(heap, origin, color)
		if done & 0xFFFF == 0:
			p = float(done)/256**3
			sys.stderr.write('\rPreprocessing: {0:.2%} done'.format(p))
			sys.stderr.flush()
	sys.stderr.write('\n')

def _add_neighbors_to_heap(heap, origin, color):
	r,g,b = color
	for dr, dg, db in (
			(-1, 0, 0),
			(+1, 0, 0),
			( 0,-1, 0),
			( 0,+1, 0),
			( 0, 0,-1),
			( 0, 0,+1),
			):
		nr = r + dr
		if nr < 0 or nr >= 256: continue
		ng = g + dg
		if ng < 0 or ng >= 256: continue
		nb = b + db
		if nb < 0 or nb >= 256: continue

		_add_to_heap(heap, origin, (nr, ng, nb))

def _add_to_heap(heap, origin, color):
	global _lookup_table

	r, g, b = color
	if _lookup_table[r][g][b] != -1:
		return

	dist_sqr = color_distance_sqr(average_colors[origin], color)

	heapq.heappush(heap, (dist_sqr, origin, color))


_load_lookup_table()

if not _lookup_table:
	_init_lookup_table()
	_save_lookup_table()
