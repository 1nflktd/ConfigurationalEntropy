from ase.visualize import view
from ase.io import write, read
from ase.neighborlist import neighbor_list
from ase.neighborlist import NeighborList

slab = read("../../graph_files/sc.xyz")

# slab.get_atomic_numbers()
# ase.data.covalent_radii[29] # 29 'Cu' # 1.32

#cutoff_radii = 1.32 * 2 * 1.20
cutoff_radii = 1.32 * 1.10
#cutoff_radii = 5
cutoff = [cutoff_radii] * len(slab)
nl = NeighborList(cutoff, bothways=True) # , self_interaction=False
nl.update(slab)

for i in range(0, len(slab)):
	indices, offsets = nl.get_neighbors(i)
	print(indices)
	print(offsets)

print(slab.get_all_distances(mic=True))
"""
print(slab.get_all_distances(mic=False))
"""
#print(neighbor_list('d', slab, cutoff_radii))

view(slab)
