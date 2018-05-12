import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import operator

from ase import Atoms
from ase.visualize import view
from ase.io import read
from ase.data import covalent_radii

slab = read("pyridine.xyz")

covalent_radii_cut_off = 1.12 # parameter

# get_distance(a1, a2)
# get_all_distances()
# get_atomic_numbers (for covalent_radii)

graph = nx.Graph()

atomic_numbers = slab.get_atomic_numbers()
for atom1, distance in enumerate(slab.get_all_distances()):
	#print(atom1)
	atom1_cr = covalent_radii[atomic_numbers[atom1]]
	for atom2, value in enumerate(distance):
		if atom1 != atom2:
			#print(atom2, value)
			atom2_cr = covalent_radii[atomic_numbers[atom2]]
			# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.[2]
			if (slab.get_distance(atom1, atom2) < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
				graph.add_edge(atom1, atom2)

	#print("")

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

x_rand = random.uniform(dmin[0], dmax[0])
y_rand = random.uniform(dmin[1], dmax[1])
z_rand = random.uniform(dmin[2], dmax[2])

distances = {}
for idx, distance in enumerate(slab.get_positions()):
	distances[idx] = math.sqrt((x_rand - distance[0]) ** 2 + (y_rand - distance[1]) ** 2 + (z_rand - distance[2]) ** 2)

print("Point: %f %f %f\n" % (x_rand, y_rand, z_rand))

print("Distances")
print(distances)
print("")
print("dmax, dmin")
print(dmax, dmin)

orderedDistances = sorted(distances.items(), key=operator.itemgetter(1))

subGraph = nx.Graph()

n = 4 # 4 neighbors
print("Distances ordered")
i = 0
nClosestNeighbors = []
for node, distance in orderedDistances:
	if i >= n:
		break

	print("%d : %f" % (node, distance))
	i += 1
	nClosestNeighbors.append(node)

for node in nClosestNeighbors:
	for neighbor in graph[node]:
		if neighbor in nClosestNeighbors:
			subGraph.add_edge(node, neighbor)

view(slab)
plt.figure(1)
nx.draw(graph, with_labels=True)
plt.figure(2)
nx.draw(subGraph, with_labels=True)
plt.show()
