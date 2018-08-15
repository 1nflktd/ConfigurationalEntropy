import sys
import matplotlib.pyplot as plt
import os

from datetime import datetime
from ase import Atom
from ase.io import read
from ase.data import covalent_radii
from math import log
from operator import itemgetter
from random import uniform
from numpy import asarray
from numpy.polynomial.polynomial import polyfit

# python2 py_nearest_neighbors.py ../../../../python/graph_files/fcc.xyz

def getMaxMinSlab():
	(dmin, dmax) = (
		{ 0:  0, 1:  0, 2:  0 },  # x, y, z
		{ 0: 3.83, 1: 8.11, 2: 10.43 }   # x, y, z
	)

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

	print n_first

	return [i[0] for i in n_first] # return only the first element in list

def main():

	filename = sys.argv[1]

	print("Starting script...")

	slab = read(filename)

	print slab

	print("Slab %s read with success" % filename)

	(dmin, dmax) = getMaxMinSlab()
	(x, y, z) = (0, 0, 0)
	atomic_number = slab.get_atomic_numbers()[0]

	closestPoints = getNClosestNeighborsFromPoint(slab, 10, x, y, z, atomic_number)
	print closestPoints

if __name__ == "__main__":
	main()
