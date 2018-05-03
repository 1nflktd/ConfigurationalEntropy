#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <vector>
#include <string>

template <typename T>
using Vector = std::vector<T>;

template <typename T>
using Matrix = Vector<Vector<T>>;

class Graph {
	Matrix<int> matrix;
	int vertices;
	int edges;
	int label;
	int primalVertex;
	void loadFile(const std::string & path);
public:
	Graph() {}
	Graph(const std::string & path);
	inline int operator()(int row, int column) const { return this->matrix[row][column]; }
	void generateRandom();
	void addEdge(int vertex, int adjacentVertex);
	void initialize(int vertices);
	inline void setPrimalVertex(int _primalVertex) {this->primalVertex = _primalVertex; }
	inline int getPrimalVertex() const { return this->primalVertex; }
	inline void setLabel(int _label) { this->label = _label; }
	inline int getLabel() const { return this->label; }
	inline int getVertices() const { return this->vertices; };
	inline int getEdges() const { return this->edges; };
	void print();
};

#endif