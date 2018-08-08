import boost_graph as bg

g = bg.Graph()
g.add_node(2)
g.add_node(3)
g.add_node(4)
g.add_node(5)
g.add_edge(2, 3)
g.add_edge(2, 4)
g.add_edge(4, 5)
g.add_edge(6, 7)
g.add_node(10)
print g.has_node(2)
print g.has_node(8)
print g.has_neighbor(2, 3)
print g.has_neighbor(6, 7)
print g.has_neighbor(2, 5)
print g.has_neighbor(4, 4)
g.print_graph()

"""
g1 = bg.Graph()
g1.add_edge(1, 2);
g1.add_edge(2, 3);
g1.add_edge(3, 4);

g2 = bg.Graph()
g2.add_edge(1, 2);
g2.add_edge(1, 3);
g2.add_edge(3, 4);

print bg.is_isomorphic(g1, g2)

print g1.get_neighbors(2)
print g1.get_neighbors(4)
print g1.get_neighbors(3)
print g1.get_neighbors(1)
print g2.get_neighbors(1)
print g2.get_neighbors(6)
"""
