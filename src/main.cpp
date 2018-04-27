#include <iostream>

#include "Graph.hpp"
#include "Method.hpp"

int main() {
	Graph graph("grafo1.x");

	Method method(graph);
	int m = 0;
	int n = 0;
	method.run(m, n);

	return 0;
}