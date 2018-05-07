import sys
import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import math

def generateSubgraphs(G, m, n):
	graphs = []
	generatedVertices = []

	i = 0
	while i < m:
		vertex = rd.randint(0, len(G.nodes) - 1) # random number

		if vertex in generatedVertices:
			continue

		generatedVertices.append(vertex)

		graph = nx.Graph(isoLabel=0)

		vertexPositions = [vertex]
		visitedVertices = {}
		neighborsFound = [0] # workaround to pass by reference

		searchNeighbors(G, vertex, m, n - 1, graph, vertexPositions, neighborsFound, visitedVertices)

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
			else:
				posInserted = vertexPositions.index(v)

			graph.add_edge(posVertex, posInserted)
			graph.node[posInserted]["originalLabel"] = v
			graph.node[posVertex]["originalLabel"] = vertex

		v += 1

	if neighborsFound[0] < n:
		# found not visited neighboor
		for v in vertexPositions:
			if v not in visitedVertices or not visitedVertices[v]:
				searchNeighbors(G, v, m, n, graph, vertexPositions, neighborsFound, visitedVertices)


def printGraph(graph):
	originalLabels = {}
	for node in graph.nodes:
		originalLabels[node] = graph.node[node]["originalLabel"]

	nx.draw(graph, with_labels=True, labels=originalLabels)
	plt.show()

def run(G, m, n):
	graphs = generateSubgraphs(G, m, n)

	graphsLabelQty = {}
	isoLabel = 1
	for i in range(len(graphs)):
		for j in range(i + 1, len(graphs)):
			if nx.is_isomorphic(graphs[i], graphs[j]):
				isoLabelGi = graphs[i].graph["isoLabel"]
				isoLabelGj = graphs[j].graph["isoLabel"]

				if isoLabelGi == 0 and isoLabelGj == 0:
					graphs[i].graph["isoLabel"] = isoLabel
					graphs[j].graph["isoLabel"] = isoLabel
					graphsLabelQty[isoLabel] = 2
					isoLabel += 1 # label already used
				elif isoLabelGi > 0 and isoLabelGj == 0:
					graphs[j].graph["isoLabel"] = isoLabelGi
					graphsLabelQty[isoLabelGi] += 1
				elif isoLabelGj > 0 and isoLabelGi == 0:
					graphs[i].graph["isoLabel"] = isoLabelGj
					graphsLabelQty[isoLabelGj] += 1
				elif isoLabelGi != isoLabelGj:
					# throw error ?
					print("Error while checking isomorphism:\nlabelGi %d : labelGj %d" % (isoLabelGi, isoLabelGj))
					print("gi", graphs[i].edges)
					print("gj", graphs[j].edges)

	shannonEntropy = 0
	for i in range(1, isoLabel):
		pi = float(graphsLabelQty[i]) / m
		shannonEntropy -= pi * math.log(pi)

	print("Different graph topologies %d" % (isoLabel - 1))
	print("Shannon entropy %f" % shannonEntropy)

def main():
	G = nx.read_adjlist("files/graph1.x", nodetype=int)
	G = nx.convert_node_labels_to_integers(G, 0)

	n = 12
	m = 10
	run(G, m, n)

if __name__ == "__main__":
	main()
