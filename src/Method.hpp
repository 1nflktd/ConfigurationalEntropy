#ifndef METHOD_HPP
#define METHOD_HPP

#include <map>

#include "Graph.hpp"

class Method {
	Graph graph;
public:
	Method(const Graph & _graph) : graph(_graph) {}
	void run(int m, int n);
	void searchNeighboors(int vertex, int n, int m, Graph & graph, Vector<int> & vertexPositions, int & neighboorsFound, std::map<int, bool> & visitedVertices);
	Vector<Graph> generateGraphs(int m, int n);
	bool checkIsomorphism(const Graph & graph1, const Graph & graph2);
};

#endif