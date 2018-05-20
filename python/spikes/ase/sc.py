from ase.lattice.cubic import SimpleCubic
from ase.visualize import view
from ase.io import write

size = (4, 5, 1)
#size = (2, 2, 1)
atoms = SimpleCubic(directions=[[1,-1,0], [1,1,0], [1,1,1]],
                    size=size, symbol='Cu', pbc=(1,1,0), latticeconstant=3.0)

view(atoms)
write("sc.xyz", atoms)
#print(atoms.get_positions())
#print(atoms.get_positions(wrap=True))
