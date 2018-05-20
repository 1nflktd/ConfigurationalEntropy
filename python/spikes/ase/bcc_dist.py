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
#write("bcc.xyz", atoms)

"""
print(atoms.get_positions())
print(atoms.get_cell())
print(atoms.get_all_distances())
"""

(dmin, dmax) = getMaxMinSlab(atoms)
(x, y, z) = generateRandomPoint(dmin, dmax)

UC = atoms.get_cell()

print("distancias para ponto")
print(UC)

for idx, p2 in enumerate(atoms.get_positions()):
	dx = x - p2[0]
	if (abs(dx) > UC[0]*0.5):
		dx = UC[0] - dx
	dy = y - p2[1]
	if (abs(dy) > UC[1]*0.5):
		dy = UC[1] - dy
	dz = z - p2[2]
	if (abs(dz) > UC[2]*0.5):
		dz = UC[2] - dz

	d = math.sqrt(dx**2 + dy**2 + dz**2)
	print(idx, d)

print('after')

atoms.append(Atom('Cu', (x, y, z)))

"""
view(atoms)
print(atoms.get_positions())
print(atoms.get_cell())
print(atoms.get_all_distances())
"""

print(atoms.get_all_distances(mic=True)[len(atoms) - 1])
atoms.pop()

"""
view(atoms)
"""