#include <fstream>
#include <algorithm>
#include <sstream>

#include "Graph.hpp"

Graph::Graph(const std::string & path) {
	this->loadFile(path);
}

void Graph::initialize(int vertices) {
	this->vertices = vertices;
	this->edges = 0;
	this->matrix = Matrix<int>(vertices, Vector<int>(vertices, -1)); // initialize all as -1 (no connection)
}

void Graph::addEdge(int vertex, int adjacentVertex) {
	if (vertex < 0 || vertex >= this->vertices)	{
		return; // throw error
	}

	if (adjacentVertex < 0 || adjacentVertex >= this->vertices) {
		return; // throw error
	}

	this->matrix[vertex][adjacentVertex] = 1;
	this->edges += 2;
	this->matrix[adjacentVertex][vertex] = 1;
}

void Graph::loadFile(const std::string & path) {
	std::ifstream infile{path, std::ios::binary};

	if (!infile) {
		throw std::runtime_error("Nao foi possível abrir o arquivo\n");
	}

	int vertices;
	infile >> vertices;

	this->initialize(vertices);

	int vertex = 0;
	std::string line;
	while (std::getline(infile, line)) {
		if (std::all_of(line.begin(), line.end(), [](char c) {
				return std::isspace(static_cast<unsigned char>(c));
			})
		) continue;

		std::istringstream iss(line);
		int n_adjacentVertices;
		iss >> n_adjacentVertices;

		for (int i = 0; i < n_adjacentVertices; ++i) {
			int adjacentVertice;
			iss >> adjacentVertice;

			this->addEdge(vertex, --adjacentVertice);
		}

		++vertex;
	}}

void Graph::generateRandom() {
	;
}
