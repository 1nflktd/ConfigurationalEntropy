import matplotlib.pyplot as plt
import networkx as nx

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

view(slab)
nx.draw(graph, with_labels=True)
plt.show()
