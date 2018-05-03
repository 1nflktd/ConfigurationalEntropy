import sys
import networkx as nx
import matplotlib.pyplot as plt

def generateSubgraphs(G, m, n):
	graphs = []
	generatedVertices = []

	i = 0
	while i < m:
		vertex = i # random number

		if vertex in generatedVertices:
			continue

		generatedVertices.append(vertex)

		graph = nx.Graph()
		vertexPositions = [vertex]
		visitedVertices = {}
		neighborsFound = [0] # workaround to pass by reference

		searchNeighbors(G, vertex, m, n, graph, vertexPositions, neighborsFound, visitedVertices)

		graphs.append(graph)
		i += 1

	return graphs


def searchNeighbors(G, vertex, m, n, graph, vertexPositions, neighborsFound, visitedVertices):
	if neighborsFound[0] >= n:
		return

	if vertex in visitedVertices and visitedVertices[vertex]:
		return

	if vertex not in vertexPositions:
		return

	posVertex = vertexPositions.index(vertex)
	visitedVertices[vertex] = True

	v = 0
	while True:
		if v >= G.number_of_nodes() or neighborsFound[0] >= n:
			break

		if G.has_edge(vertex, v):
			if v not in vertexPositions:
				neighborsFound[0] += 1

				vertexPositions.append(v)

				posInserted = len(vertexPositions) - 1

				graph.add_edge(posVertex, posInserted)
			else:
				pos = vertexPositions.index(v)
				graph.add_edge(posVertex, pos)

		v += 1

	if neighborsFound[0] < n:
		# found not visited neighboor
		for v in vertexPositions:
			if v not in visitedVertices or not visitedVertices[v]:
				searchNeighbors(G, v, m, n, graph, vertexPositions, neighborsFound, visitedVertices)


def run(G, m, n):
	# nx.draw(G, with_labels=True)
	# plt.show()

	graphs = generateSubgraphs(G, m, n)

	for g in graphs:
		nx.draw(g, with_labels=True)
		plt.show()

def main():
	G = nx.read_adjlist("files/graph1.x")
	G = nx.convert_node_labels_to_integers(G, 0)
	n = 3
	m = 4
	run(G, m, n)

if __name__ == "__main__":
	main()
