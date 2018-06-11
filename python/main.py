import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import ase
import ase.io
import ase.data
import ase.visualize
import operator
import numpy as np
from numpy.polynomial.polynomial import polyfit
from multiprocessing import Process, Queue

def run(q, G, m, n, slab, c):
	graphs = generateSubgraphs(G, m, n, slab)

	label_total = {}
	iso_label = 1
	for i in range(len(graphs)):
		for j in range(i + 1, len(graphs)):
			iso_label_i = graphs[i].graph["isoLabel"]
			iso_label_j = graphs[j].graph["isoLabel"]
			
			if iso_label_i == 0 or iso_label_j == 0:
				if nx.is_isomorphic(graphs[i], graphs[j]):
					if iso_label_i == 0 and iso_label_j == 0:
						# printGraph(graphs[i])

						graphs[i].graph["isoLabel"] = iso_label
						graphs[j].graph["isoLabel"] = iso_label
						label_total[iso_label] = 2
						iso_label += 1 # label already used
					elif iso_label_i > 0 and iso_label_j == 0:
						graphs[j].graph["isoLabel"] = iso_label_i
						label_total[iso_label_i] += 1
					elif iso_label_j > 0 and iso_label_i == 0:
						graphs[i].graph["isoLabel"] = iso_label_j
						label_total[iso_label_j] += 1
					elif iso_label_i != iso_label_j:
						# throw error ?
						print("Error while checking isomorphism:\nlabelGi %d : labelGj %d" % (iso_label_i, iso_label_j))
						print("gi", graphs[i].edges)
						print("gj", graphs[j].edges)

	# get all graphs that are not isomorphic with any other
	for g in graphs:
		if g.graph["isoLabel"] == 0:
			label_total[iso_label] = 1
			iso_label += 1

	H_n = 0.0
	H1n = 0.0
	for i in range(1, iso_label):
		fi = float(label_total[i])
		H_n = calcShannonEntropy(H_n, fi, m)
		if fi == 1.0:
			H1n = calcShannonEntropy(H1n, fi, m)

	H1nDiv = 0.0
	if H_n > 0:
		H1nDiv = (H1n / H_n)

	H_n_extrapolated = H_n + (c * H1nDiv)
	# dimensions always = 3 ?
	spatial_dimensions = 3
	g_n = (spatial_dimensions - 1) * math.log(n)
	Hc_n = H_n - g_n

	#print("label_total ", label_total)
	"""
	print("Different graph topologies %d" % (iso_label - 1))
	print("Shannon entropy: H(n) = %f" % H_n)
	print("H1(n) = %f" % H1n)
	print("Extrapolated H(n) = %f" % H_n_extrapolated)
	print("g(n) = %f" % g_n)
	print("Corrected H(n) = %f" % Hc_n)
	if H1n > (H_n / 100): # se H1n exceder 1% de H_n, nao e uma amostra valida
		print("H1(n) exceeds 1% of H(n). Not a valid measurement.")
	"""

	q.put((n, Hc_n))

	return Hc_n

def calcShannonEntropy(Hn, fi, m):
	pi = fi / m
	Hn -= pi * math.log(pi)
	return Hn

def generateSubgraphs(G, m, n, slab):
	graphs = []

	(dmin, dmax) = getMaxMinSlab(slab)

	i = 0
	while i < m:
		(x, y, z) = generateRandomPoint(dmin, dmax)
		n_closest_neighbors = getNClosestNeighborsFromPoint(slab, n, x, y, z)

		# print(x, y, z)

		graph = generateSubGraph(G, n, n_closest_neighbors)

		# printGraph(graph)

		graphs.append(graph)
		i += 1

	return graphs

def getMaxMinSlab(slab):
	(dmin, dmax) = (
		{ 0:  float("Inf"), 1:  float("Inf"), 2:  float("Inf") },  # x, y, z
		{ 0: -float("Inf"), 1: -float("Inf"), 2: -float("Inf") }   # x, y, z
	)

	positions = slab.get_positions(wrap=True) # wrap atoms back to simulation cell ? default: wrap=False
	for distance in positions:
		for idx, d in enumerate(distance):
			if (d > dmax[idx]):
				dmax[idx] = d
			if (d < dmin[idx]):
				dmin[idx] = d

	return (dmin, dmax)

def generateRandomPoint(dmin, dmax):
	x = random.uniform(dmin[0], dmax[0])
	y = random.uniform(dmin[1], dmax[1])
	z = random.uniform(dmin[2], dmax[2])

	return (x, y, z)

def getNClosestNeighborsFromPoint(slab, n, x, y, z):
	slab.append(ase.Atom('Cu', (x, y, z)))
	idxAtom = len(slab) - 1
	all_distances = slab.get_all_distances(mic=True)[idxAtom]
	# all_distances = slab.get_all_distances()[idxAtom]
	slab.pop()

	distances = {}
	for idx, distance in enumerate(all_distances):
		if idx == idxAtom:
			break
		distances[idx] = distance

	n_first = sorted(distances.items(), key=operator.itemgetter(1))[:n] # return list of tuples
	return [i[0] for i in n_first] # return only the first element in list

def generateSubGraph(G, n, n_closest_neighbors):
	graph = nx.Graph(isoLabel=0)

	for node in n_closest_neighbors:
		if node in G:
			if node not in graph:
				graph.add_node(node)

			for neighbor in G[node]:
				if neighbor in n_closest_neighbors:
					graph.add_edge(node, neighbor)

	# printGraph(graph)

	return graph

def generateGraphFromSlab(slab, covalent_radii_cut_off):
	graph = nx.Graph()

	atomic_numbers = slab.get_atomic_numbers()
	# all_distances = slab.get_all_distances()
	all_distances = slab.get_all_distances(mic=True)
	for atom1, distances in enumerate(all_distances):
		if atom1 not in graph:
			graph.add_node(atom1) # add nodes not bonded

		atom1_cr = ase.data.covalent_radii[atomic_numbers[atom1]]
		for atom2, distance in enumerate(distances):
			if atom1 != atom2:
				atom2_cr = ase.data.covalent_radii[atomic_numbers[atom2]]
				# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
				if (distance < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
					graph.add_edge(atom1, atom2)

	return graph

def printGraph(graph):
	nx.draw(graph, with_labels=True)
	plt.show()

def main():
	if len(sys.argv) < 6:
		print("1 parameter: xyz filename\n2 parameter: covalent_radii_cut_off\n3 parameter: c\n4 parameter: initial n\n5 parameter: final n")
		return

	filename = sys.argv[1]
	covalent_radii_cut_off = float(sys.argv[2]) # 1.12
	c = float(sys.argv[3])
	n1 = int(sys.argv[4])
	n2 = int(sys.argv[5])

	if n1 > n2:
		print("Final m cannot be smaller than initial m")
		return

	print("Starting script...")

	slab = ase.io.read(filename)

	print("Slab %s read with success" % filename)

	# ase.visualize.view(slab)

	G = generateGraphFromSlab(slab, covalent_radii_cut_off)
	total_nodes = len(G)
	if total_nodes == 0:
		print("No nodes found in graph. Check covalent_radii_cut_off")
		return

	print("Graph created with success. Nodes found: %d" % total_nodes)

	q = Queue()
	processes = []
	for n in range(n1, n2):
		m = 3.4 * (n * n) * total_nodes

		# print("Parameters used:\nGraph = %s\nm = %d\nn = %d\nCovalent radii cut off = %f\nc = %f" % (filename, m, n, covalent_radii_cut_off, c))

		# printGraph(G)

		# hcn = run(G, m, n, slab, c)
		p = Process(target=run, args=(q, G, m, n, slab, c, ))
		p.start()
		processes.append(p)

		# print("n = %f, Hc(n) = %f" % (n, hcn))

	hcn_values = []
	for p in processes:
		n, hcn = q.get()
		n = int(n)
		hcn_values.append((n, hcn))
		print("n = %d, Hc(n) = %f" % (n, hcn))

	for p in processes:
		p.join()

	x, y = zip(*hcn_values)
	x = np.asarray(x)
	y = np.asarray(y)
	# straight line fit
	b, m = polyfit(x, y, 1) # m equals the slope of the line
	plt.scatter(x, y)
	plt.plot(x, b + m * x, '-')
	plt.axis([n1, n2, -2, 10])
	plt.show()

	print("Estimated configurational entropy = %f" % (m))


if __name__ == "__main__":
	main()
