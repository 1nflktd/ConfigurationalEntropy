#include <iostream>
#include <limits>

#include "Graph.hpp"
#include "Method.hpp"

void readInputClear() {
	std::cin.clear(); //clear bad input flag
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //discard input
	std::cout << "Invalid input. Type again.\n";
}

int main() {
	std::string filename;
	while (((std::cout << "Type the filename of a graph: ") && !(std::cin >> filename)))
		readInputClear();

	int n, m;
	while (((std::cout << "Type n m: ") && !(std::cin >> n >> m)) || (n <= 0 || m <= 0))
		readInputClear();

	Graph graph(filename);
	Method method(graph);
	method.run(m, n);

	return 0;
}