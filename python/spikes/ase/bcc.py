from ase.lattice.cubic import BodyCenteredCubic
from ase.visualize import view
from ase.io import write
from ase import Atom
import random
import math

def getMaxMinSlab(slab):
	(dmin, dmax) = (
		{ 0:  float("Inf"), 1:  float("Inf"), 2:  float("Inf") },  # x, y, z
		{ 0: -float("Inf"), 1: -float("Inf"), 2: -float("Inf") }   # x, y, z
	)

	positions = slab.get_positions()
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


atoms = BodyCenteredCubic(directions=[[1,0,0], [0,1,0], [1,1,1]], size=(3,3,4), symbol='Cu', pbc=(1,1,0), latticeconstant=4.0)

view(atoms)
write("bcc.xyz", atoms)

"""
print(atoms.get_positions())
print(atoms.get_cell())
print(atoms.get_all_distances())

(dmin, dmax) = getMaxMinSlab(atoms)
(x, y, z) = generateRandomPoint(dmin, dmax)

print("distancias para ponto")
for idx, distance in enumerate(atoms.get_positions()):
	d = math.sqrt((x - distance[0]) ** 2 + (y - distance[1]) ** 2 + (z - distance[2]) ** 2)
	print(idx, d)

atoms.append(Atom('Cu', (x, y, z)))

print('after')

view(atoms)
print(atoms.get_positions())
print(atoms.get_cell())
print(atoms.get_all_distances())

print(atoms.get_all_distances(mic=True)[12])
atoms.pop()
view(atoms)
"""