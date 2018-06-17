from ase.lattice.hexagonal import HexagonalClosedPacked
from ase.visualize import view
from ase.io import write

atoms = HexagonalClosedPacked(size=(3,3,2), symbol='Ti', pbc=(1,1,0))

view(atoms)
#write("hcp.xyz", atoms)
#print(atoms.get_positions())
#print(atoms.get_positions(wrap=True))
