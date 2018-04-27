#ifndef METHOD_HPP
#define METHOD_HPP

#include "Graph.hpp"

class Method {
	Graph graph;
public:
	Method(const Graph & _graph) : graph(_graph) {}
	void run(int m, int n);
	void searchNeighboors(int vertex, Graph & graph);
	Vector<Graph> generateGraphs(int m, int n);
	void checkIsomorphism(const Graph & graph1, const Graph & graph2);
};

#endif