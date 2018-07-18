import boost_graph

g = boost_graph.Graph()
g.add_node(2)
g.add_node(3)
g.add_node(4)
g.add_node(5)
g.add_edge(2, 3)
g.add_edge(2, 4)
g.has_node(2)
g.has_neighbor(2, 3)
g.printG()
