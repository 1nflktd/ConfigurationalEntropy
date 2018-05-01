#include <algorithm>
#include <random>
#include <iostream>

#include "Method.hpp"

void Method::run(int m, int n) {
	Vector<Graph> graphs = this->generateGraphs(m, n);

	int label = 1;
	for (int i = 0; i < m; ++i) {
		for (int j = i; j < m; ++j) {
			if (i != j) {
				if (this->isIsomorph(graphs[i], graphs[j])) {
					// add graphs[i] count ++;
					int labelGi = graphs[i].getLabel();
					int labelGj = graphs[j].getLabel();
					if (labelGi == 0 && labelGj == 0) {
						graphs[i].setLabel(label);
						graphs[j].setLabel(label);
						++label; // label already used
					} else if (labelGi > 0 && labelGj == 0) {
						graphs[j].setLabel(labelGi);
					} else if (labelGj > 0 && labelGi == 0) {
						graphs[i].setLabel(labelGj);
					} else if (labelGi != labelGj) {
						// throw error ?
						std::cout << "errr something went wrong: labelGi " << labelGi << " labelGj " << labelGj << "\n";
						std::cout << "g(i)->primalVertex: " << graphs[i].getPrimalVertex() << "\ng(j)->primalVertex: " << graphs[j].getPrimalVertex() << "\n";
						std::cout << "graph(i)\n";
						graphs[i].print();
						std::cout << "graph(j)\n";
						graphs[j].print();
					}
				}
			}
		}
	}

	std::cout << "Different graph topologies " << (label - 1) << "\n";
}

Vector<Graph> Method::generateGraphs(int m, int n) {
	Vector<Graph> graphs(m); // m graphs

	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis(0, this->graph.getVertices() - 1); // [0, size]

	Vector<int> generatedVertices(m);

	int nGraph = 0;
	while (nGraph < m) {
		// random position
		int vertex = dis(gen);

		// to not repeat
		if (std::find(generatedVertices.begin(), generatedVertices.end(), vertex) != generatedVertices.end()) {
			continue;
		}

		generatedVertices.push_back(vertex);

		Graph graph;
		graph.initialize(n + 1);
		graph.setPrimalVertex(vertex);

		Vector<int> vertexPositions; // ex: 0 -> 101, 1 -> 97, etc.
		vertexPositions.push_back(vertex);

		std::map<int, bool> visitedVertices;

		int neighboorsFound = 0;

		this->searchNeighboors(vertex, n, m, graph, vertexPositions, neighboorsFound, visitedVertices);

		graphs[nGraph] = graph;

		std::cout << "vertex: " << vertex << "\n";
		graph.print();

		++nGraph;
	}

	return graphs;
}

bool Method::isIsomorph(const Graph & graph1, const Graph & graph2) {
	if (graph1.getVertices() != graph2.getVertices() || graph1.getEdges() != graph2.getEdges()) {
		return false;
	}

	Vector<int> map(graph1.getVertices());
	std::iota(map.begin(), map.end(), 0); // 0, 1, 2, 3, up to N
	do
	{
		if (this->checkIsomorphism(graph1, graph2, map)) {
			return true;
		}
	} while (std::next_permutation(map.begin(), map.end()));

	return false;
}

bool Method::checkIsomorphism(const Graph & graph1, const Graph & graph2, const Vector<int> & map) {
	int N = graph1.getVertices();
	for (int i = 0; i < N; ++i)
		for (int j = 0; j < N; ++j)
			if (graph1(i, j) != graph2(map[i], map[j])) return false;
	return true;
}

void Method::searchNeighboors(int vertex, int n, int m, Graph & graph, Vector<int> & vertexPositions, int & neighboorsFound, std::map<int, bool> & visitedVertices) {
	if (neighboorsFound >= n) {
		return;
	}

	if (visitedVertices[vertex]) {
		return;
	}

	auto itVertex = std::find(vertexPositions.begin(), vertexPositions.end(), vertex);
	if (itVertex == vertexPositions.end()) {
		return;
	}

	int posVertex = std::distance(vertexPositions.begin(), itVertex);
	visitedVertices[vertex] = true;

	for (int v = 0; v < this->graph.getVertices() && neighboorsFound < n; ++v) {
		if (this->graph(vertex, v) == 1) {
			auto itI = std::find(vertexPositions.begin(), vertexPositions.end(), v);
			if  (itI == vertexPositions.end()) {
				++neighboorsFound;

				vertexPositions.push_back(v);

				auto posInserted = vertexPositions.size() - 1;

				graph.addEdge(posVertex, posInserted);
			} else {
				int posI = std::distance(vertexPositions.begin(), itI);

				graph.addEdge(posVertex, posI);
			}
		}
	}

	if (neighboorsFound < n) {
		// found not visited neighboor
		for (const auto & v : vertexPositions) {
			if (!visitedVertices[v]) {
				searchNeighboors(v, n, m, graph, vertexPositions, neighboorsFound, visitedVertices);
			}
		}
	}
}
