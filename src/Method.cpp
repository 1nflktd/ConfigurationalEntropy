#include "Method.hpp"

void Method::run(int m, int n) {
	Vector<Graph> graphs = this->generateGraphs(m, n);
}

Vector<Graph> Method::generateGraphs(int m, int n) {
	Vector<Graph> graphs = Vector<Graph>(m); // m graphs

	// buscar m posicoes aleatorias
		// buscar n vizinhos

	int nGraph = 0;
	while (nGraph < m) {
		// posicao aleatoria (vertice aleatorio (?))
		int pos1 = 0;
		// achou vertice
		Graph graph;
		graph.initialize(n + 1); // nao vai ter esse nro necessariamente
		// buscar n vizinhos
		this->searchNeighboors(pos1, graph);
		graphs[nGraph] = graph;
		++nGraph;
	}

	return graphs;
}

void Method::checkIsomorphism(const Graph & graph1, const Graph & graph2) {
	;
}

void Method::searchNeighboors(int vertex, Graph & graph) {
	// essa funcao tem que ser recursiva, ate n+1

	int nVertices = graph.getVertices();
	// 1 level
	int neighboors = 0;
	for (int i = 0; i < nVertices && neighboors < nVertices; ++i) {
		if (this->graph(vertex, i) == 1) {
			graph.addEdge(vertex, i); // ERRADO, tem que comecar do 0 (vertex pode ser qualquer valor)
		}
	}
}
