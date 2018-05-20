from ase.lattice.cubic import FaceCenteredCubic
from ase.visualize import view
from ase.io import write

atoms = FaceCenteredCubic(directions=[[1,-1,0], [1,1,-2], [1,1,1]],
                           size=(2,2,2), symbol='Cu', pbc=(1,1,0))

view(atoms)
write("fcc.xyz", atoms)
#print(atoms.get_positions())
#print(atoms.get_positions(wrap=True))
