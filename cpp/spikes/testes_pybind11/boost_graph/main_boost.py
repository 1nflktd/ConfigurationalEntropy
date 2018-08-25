import sys
import boost_graph as bg
import matplotlib.pyplot as plt
import os
import aboria_nnsearch as aboria

from datetime import datetime
from ase import Atom
from ase.io import read
from ase.data import covalent_radii
from math import log
from operator import itemgetter
from random import uniform
from numpy import asarray
from numpy.polynomial.polynomial import polyfit

def run(G, m, n, slab, c, atomic_number, aboria_tree):
	graphs = bg.Graphs(m)

	generateSubgraphs(G, graphs, m, n, slab, atomic_number, aboria_tree)
	Hc_n, valid = graphs.check_isomorfism(n, m, c)

	if not valid:
		print("n: %d. H1(n) exceeds 1%% of H(n). Not a valid measurement." % n)

	return Hc_n, valid

def generateSubgraphs(G, graphs, m, n, slab, atomic_number, aboria_tree):
	(dmin, dmax) = getMaxMinSlab(slab)

	closest_neighbors = []
	for i in range(m):
		(x, y, z) = generateRandomPoint(dmin, dmax)
		n_closest_neighbors = aboria_tree.search_nearest_neighbors(x, y, z, n)
		closest_neighbors.append(n_closest_neighbors)

	graphs.generate_subgraphs(G, n, closest_neighbors)

def getMaxMinSlab(slab):
	"""
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

	"""
	cell = slab.get_cell()
	dmin = {0: 0, 1: 0, 2: 0};
	dmax = {0: cell[0][0], 1: cell[1][1], 2: cell[2][2]}
	return (dmin, dmax)

def generateRandomPoint(dmin, dmax):
	x = uniform(dmin[0], dmax[0])
	y = uniform(dmin[1], dmax[1])
	z = uniform(dmin[2], dmax[2])

	return (x, y, z)

def getAllDistancesFromPoint(slab, atomic_number, x, y, z):
	slab.append(Atom(atomic_number, (x, y, z))) # get the first atom
	idx_atom = len(slab) - 1
	indices = range(0, idx_atom)
	all_distances = slab.get_distances(idx_atom, indices, mic=True)
	slab.pop()

	return all_distances

def getNClosestNeighborsFromPoint(slab, n, x, y, z, atomic_number):
	all_distances = getAllDistancesFromPoint(slab, atomic_number, x, y, z)
	distances = dict((idx, d) for idx, d in enumerate(all_distances))
	n_first = sorted(distances.items(), key=itemgetter(1))[:n]
	return [i[0] for i in n_first] # return only the first element in list

def generateGraphFromSlab(slab, covalent_radii_cut_off):
	graph = bg.Graph()

	atomic_numbers = slab.get_atomic_numbers()
	all_distances = slab.get_all_distances(mic=True)
	for atom1, distances in enumerate(all_distances):
		if not graph.has_node(atom1):
			graph.add_node(atom1) # add nodes not bonded

		atom1_cr = covalent_radii[atomic_numbers[atom1]]
		for atom2, distance in enumerate(distances):
			if atom1 != atom2:
				atom2_cr = covalent_radii[atomic_numbers[atom2]]
				# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
				if (distance < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
					graph.add_edge(atom1, atom2)

	return graph

def main():
	if len(sys.argv) < 7:
		print("1 parameter: xyz filename\n2 parameter: covalent_radii_cut_off\n3 parameter: c\n4 parameter: initial n\n5 parameter: final n\n6 parameter: calculate (Y or N)")
		return

	filename = sys.argv[1]
	covalent_radii_cut_off = float(sys.argv[2]) # 1.12
	c = float(sys.argv[3])
	n1 = int(sys.argv[4])
	n2 = int(sys.argv[5])
	calculate = sys.argv[6] # Y or N

	if n1 > n2:
		print("Final m cannot be smaller than initial m")
		return

	print("Starting script...")

	slab = read(filename)

	print("Slab %s read with success" % filename)

	G = generateGraphFromSlab(slab, covalent_radii_cut_off)
	total_nodes = G.get_total_nodes()
	if total_nodes == 0 or G.get_total_edges() == 0:
		print("No edges found in graph. Check covalent_radii_cut_off")
		return

	print("Graph created with success. Nodes found: %d" % total_nodes)

	date_now = datetime.now()
	ce_file = "generated_files/gen_" + str(date_now.day) + "_" + str(date_now.month) + "_" + str(date_now.year) + "_" + str(date_now.hour) + "_" + str(date_now.minute) + "_" + str(date_now.second) + ".ce"
	dirname = os.path.dirname(ce_file)
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	f = open(ce_file, "w+")
	f.write("filename: " + filename + "; covalent: " + str(covalent_radii_cut_off) + "; c: " + str(c) + "; n1: " + str(n1) + "; n2: " + str(n2) + "\r\n")

	hcn_values = []
	xy_polyfit = []
	atomic_number = slab.get_atomic_numbers()[0]

	(pbcX, pbcY, pbcZ) = slab.get_pbc()
	aboria_tree = aboria.SearchTree(3, len(slab), pbcX, pbcY, pbcZ)
	aboria_tree.add_positions(slab.get_positions(wrap=True))
	cell = slab.get_cell()
	aboria_tree.init_search(0, cell[0][0], 0, cell[1][1], 0, cell[2][2])

	for n in range(n1, n2):
		m = n * n * total_nodes
		(hcn, valid) = run(G, m, n, slab, c, atomic_number, aboria_tree)

		f.write("n: " + str(n) + "; m: " + str(m) + "; hcn: " + str(hcn) + "; valid: " + str(valid) + "\r\n")

		hcn_values.append((n, hcn))
		if valid:
			xy_polyfit.append((n, hcn))

	f.close()

	if calculate == "Y":
		(x_p, y_p) = zip(*xy_polyfit)
		x_p = asarray(x_p)
		y_p = asarray(y_p)

		# straight line fit
		b, m = polyfit(x_p, y_p, 1) # m equals the slope of the line
		plt.plot(x_p, b + m * x_p, '-')

		x, y = zip(*hcn_values)
		plt.scatter(x, y)

		plt.axis([n1, n2, -5, 10])
		plt.show()

		print("Estimated configurational entropy = %f" % (m))

	print("Program ended correctly")

if __name__ == "__main__":
	main()
