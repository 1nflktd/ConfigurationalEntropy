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

def run(G, m, n, slab):
	graphs = generateSubgraphs(G, m, n, slab)

	graphsLabelQty = {}
	isoLabel = 1
	for i in range(len(graphs)):
		for j in range(i + 1, len(graphs)):
			if nx.is_isomorphic(graphs[i], graphs[j]):
				isoLabelGi = graphs[i].graph["isoLabel"]
				isoLabelGj = graphs[j].graph["isoLabel"]

				if isoLabelGi == 0 and isoLabelGj == 0:
					graphs[i].graph["isoLabel"] = isoLabel
					graphs[j].graph["isoLabel"] = isoLabel
					graphsLabelQty[isoLabel] = 2
					isoLabel += 1 # label already used
				elif isoLabelGi > 0 and isoLabelGj == 0:
					graphs[j].graph["isoLabel"] = isoLabelGi
					graphsLabelQty[isoLabelGi] += 1
				elif isoLabelGj > 0 and isoLabelGi == 0:
					graphs[i].graph["isoLabel"] = isoLabelGj
					graphsLabelQty[isoLabelGj] += 1
				elif isoLabelGi != isoLabelGj:
					# throw error ?
					print("Error while checking isomorphism:\nlabelGi %d : labelGj %d" % (isoLabelGi, isoLabelGj))
					print("gi", graphs[i].edges)
					print("gj", graphs[j].edges)

	shannonEntropy = 0
	for i in range(1, isoLabel):
		pi = float(graphsLabelQty[i]) / m
		shannonEntropy -= pi * math.log(pi)

	print("Different graph topologies %d" % (isoLabel - 1))
	print("Shannon entropy %f" % shannonEntropy)

def generateSubgraphs(G, m, n, slab):
	graphs = []

	(dmax, dmin) = getMaxMinSlab(slab)

	i = 0
	while i < m:
		(x, y, z) = generateRandomPoint(dmax, dmin)
		orderedDistances = getOrderedDistancesFromPoint(slab, x, y, z)

		# print(x, y, z)

		graph = generateSubGraph(G, n, orderedDistances)

		# printGraph(graph)

		graphs.append(graph)
		i += 1

	return graphs

def getMaxMinSlab(slab):
	(dmax, dmin) = (
		{ 0: -float("Inf"), 1: -float("Inf"), 2: -float("Inf") }, # x, y, z
		{ 0:  float("Inf"), 1:  float("Inf"), 2:  float("Inf") }  # x, y, z
	)

	for distance in slab.get_positions():
		for idx, d in enumerate(distance):
			if (d > dmax[idx]):
				dmax[idx] = d
			if (d < dmin[idx]):
				dmin[idx] = d

	return (dmax, dmin)

def generateRandomPoint(dmin, dmax):
	x = random.uniform(dmin[0], dmax[0])
	y = random.uniform(dmin[1], dmax[1])
	z = random.uniform(dmin[2], dmax[2])

	return (x, y, z)

def getOrderedDistancesFromPoint(slab, x, y, z):
	distances = {}
	for idx, distance in enumerate(slab.get_positions()):
		distances[idx] = math.sqrt((x - distance[0]) ** 2 + (y - distance[1]) ** 2 + (z - distance[2]) ** 2)

	return sorted(distances.items(), key=operator.itemgetter(1))

def generateSubGraph(graph, n, orderedDistances):
	subGraph = nx.Graph(isoLabel=0)

	i = 0
	nClosestNeighbors = []
	for node, distance in orderedDistances:
		if i >= n:
			break
		i += 1
		nClosestNeighbors.append(node)

	for node in nClosestNeighbors:
		if node in graph:
			for neighbor in graph[node]:
				if neighbor in nClosestNeighbors:
					subGraph.add_edge(node, neighbor)

	return subGraph

def generateGraphFromSlab(slab, covalent_radii_cut_off):
	graph = nx.Graph()

	atomic_numbers = slab.get_atomic_numbers()
	for atom1, distance in enumerate(slab.get_all_distances()):
		atom1_cr = ase.data.covalent_radii[atomic_numbers[atom1]]
		for atom2, value in enumerate(distance):
			if atom1 != atom2:
				atom2_cr = ase.data.covalent_radii[atomic_numbers[atom2]]
				# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
				if (slab.get_distance(atom1, atom2) < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
					graph.add_edge(atom1, atom2)

	return graph

def printGraph(graph):
	nx.draw(graph, with_labels=True)
	plt.show()

def main():
	if len(sys.argv) < 5:
		print("1 parameter: xyz filename\n2 parameter: m\n3 parameter: n\n4 parameter: covalent_radii_cut_off")
		return

	filename = sys.argv[1]
	m = int(sys.argv[2]) # 100
	n = int(sys.argv[3]) # 8
	covalent_radii_cut_off = float(sys.argv[4]) # 1.12

	print("Parameters used:\nGraph = %s\nm = %d\nn = %d\nCovalent radii cut off = %f\n" % (filename, m, n, covalent_radii_cut_off))

	print("Starting script...")

	slab = ase.io.read(filename)

	print("slab %s read with success" % filename)

	# ase.visualize.view(slab)

	G = generateGraphFromSlab(slab, covalent_radii_cut_off)
	total_nodes = len(G)
	if total_nodes == 0:
		print("No nodes found in graph. Check covalent_radii_cut_off")
		return

	print("Total nodes: %d" % total_nodes)

	# printGraph(G)

	run(G, m, n, slab)

if __name__ == "__main__":
	main()
