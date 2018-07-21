import boost_graph

"""
g = boost_graph.Graph()
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
g.print()
"""

g1 = boost_graph.Graph()
g1.add_edge(1, 2);
g1.add_edge(2, 3);
g1.add_edge(3, 4);

g2 = boost_graph.Graph()
g2.add_edge(1, 2);
g2.add_edge(1, 3);
g2.add_edge(3, 4);

print boost_graph.is_isomorphic(g1, g2)
