import sys
import os
import aboria_nnsearch as aboria
import ase.geometry
import ase.visualize

from ase import Atom
from ase.io import read
from operator import itemgetter
from random import uniform

# python2 aboria_py_nnsearch.py ../../../../python/graph_files/fcc.xyz
# python2 aboria_py_nnsearch.py ../../../../python/graph_files/fcc_sempbc.xyz

def getMaxMinSlab(slab):
	(dmin, dmax) = (
		{ 0:  float("Inf"), 1:  float("Inf"), 2:  float("Inf") },  # x, y, z
		{ 0: -float("Inf"), 1: -float("Inf"), 2: -float("Inf") }   # x, y, z
	)

	positions = slab.get_positions(wrap=True) # wrap atoms back to simulation cell
	for distance in positions:
		for idx, d in enumerate(distance):
			if (d > dmax[idx]):
				dmax[idx] = d
			if (d < dmin[idx]):
				dmin[idx] = d

	return (dmin, dmax)

def getAllDistancesFromPoint(slab, atomic_number, x, y, z):
	slab.append(Atom(atomic_number, (x, y, z))) # get the first atom
	idxAtom = len(slab) - 1
	indices = range(0, idxAtom)
	all_distances = slab.get_distances(idxAtom, indices, mic=True)
	slab.pop()

	return all_distances

def getNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number):
	all_distances = getAllDistancesFromPoint(slab, atomic_number, x, y, z)
	distances = {}
	for idx, distance in enumerate(all_distances):
		distances[idx] = distance

	n_first = sorted(distances.items(), key=itemgetter(1))[:n] # return list of tuples

	"""
	for i, d in n_first:
		print i, "\t", d
	"""

	return [i[0] for i in n_first] # return only the first element in list

def generateRandomPoint(dmin, dmax):
	x = uniform(dmin[0], dmax[0])
	y = uniform(dmin[1], dmax[1])
	z = uniform(dmin[2], dmax[2])

	return (x, y, z)

def main():

	filename = sys.argv[1]

	print("Starting script...")

	slab = read(filename)

	print("Slab %s read with success" % filename)

	(dmin, dmax) = getMaxMinSlab(slab)
	atomic_number = slab.get_atomic_numbers()[0]

	n = 20
	(pbcX, pbcY, pbcZ) = slab.get_pbc()
	aboriaSearchTree = aboria.SearchTree(3, len(slab), pbcX, pbcY, pbcZ)
	aboriaSearchTree.add_positions(slab.get_positions(wrap=True))

	cell = slab.get_cell()
	aboriaSearchTree.init_search(0, cell[0][0], 0, cell[1][1], 0, cell[2][2])

	iguais, diferentes = 0, 0

	for i in range(1, 501):
		(x, y, z) = generateRandomPoint(dmin, dmax)
		nnPy = getNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number)
		nnAboria = aboriaSearchTree.search_nearest_neighbors(x, y, z, n)

		if (nnPy == nnAboria):
			iguais += 1
		else:
			diferentes += 1
			print x, y, z
			print "nnPy"
			#print sorted(nnPy)
			print nnPy
			print "nnAboria"
			print nnAboria
			print ""

	print "iguais %d, diferentes %d" % (iguais, diferentes)

	"""
	(x, y, z) = (2.893079307334, 1.57366629713, 6.2738712726)
	nnPy = getNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number)
	"""

if __name__ == "__main__":
	main()
