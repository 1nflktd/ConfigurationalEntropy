import sys

from ase import Atom
from ase.io import read
from operator import itemgetter

# python2 nnsearch.py ../../../../../python/graph_files/fcc.xyz

def getAllDistancesFromPoint(slab, atomic_number, x, y, z):
	slab.append(Atom(atomic_number, (x, y, z))) # append phantom atom
	idxAtom = len(slab) - 1
	indices = range(0, idxAtom)
	allDistances = slab.get_distances(idxAtom, indices, mic=True)
	slab.pop() # remove phantom

	return allDistances

def printNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number):
	allDistances = getAllDistancesFromPoint(slab, atomic_number, x, y, z)
	distances = dict((idx, d) for idx, d in enumerate(allDistances))
	nClosest = sorted(distances.items(), key=itemgetter(1))[:n]
	for i in nClosest:
		print i[0], "\t:\t", i[1]

def main():
	filename = sys.argv[1]
	x, y, z = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) # random point

	slab = read(filename)
	atomic_number = slab.get_atomic_numbers()[0]
	n = 10 # number of neighbors
	printNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number)

if __name__ == "__main__":
	main()
