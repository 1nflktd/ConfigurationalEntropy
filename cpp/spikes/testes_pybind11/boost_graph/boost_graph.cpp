#include <pybind11/pybind11.h>

#include <iostream>

#include "boost/graph/graph_traits.hpp"
#include "boost/graph/adjacency_list.hpp"

namespace py = pybind11;

/*
g++ -O3 -Wall -std=c++14 boost_graph.cpp -o boost_graph
g++ -O3 -Wall -shared -std=c++14 -I../pybind11/include -fPIC `python-config --includes` boost_graph.cpp -o boost_graph.so
*/

using Edge = std::pair<int, int>;
using Vertex = int;
using UndirectedGraph = boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, Vertex, Edge>;
//Ok, we want to see that all our edges are now contained in the graph
using edge_iterator = boost::graph_traits<UndirectedGraph>::edge_iterator;

struct Graph {
	Graph() { isoLabel = 0; graph = UndirectedGraph(); }

	inline void setIsoLabel(int _isoLabel) { isoLabel = _isoLabel; }
	inline int getIsoLabel() const { return isoLabel; }
	void add_node(int _node);
	void add_edge(int e1, int e2);
	bool has_node(int _node);
	bool has_neighbor(int node, int neighbor);
	void printG();

private:
    UndirectedGraph graph;
	int isoLabel;
};

void Graph::add_node(int _node) {
	std::cout << "add_node\n" << _node << "\n";
    boost::add_vertex(_node, this->graph);
}

void Graph::add_edge(int e1, int e2) {
	std::cout << "add_edge\n" << e1 << " " << e2 << "\n";
    boost::add_edge(e1, e2, this->graph);
}

bool Graph::has_node(int _node) {
	std::cout << "has_node\n" << _node << "\n";
	return false;
}

bool Graph::has_neighbor(int _node, int neighbor) {
	std::cout << "has_neighbor\n" << _node << " " << neighbor << "\n";
	return false;
}

void Graph::printG() {
	std::cout << "-----------------------------\n";
    std::cout << num_edges(this->graph) << "\n";

    //Tried to make this section more clear, instead of using tie, keeping all
    //the original types so it's more clear what is going on
    std::pair<edge_iterator, edge_iterator> ei = edges(this->graph);
    for (edge_iterator edge_iter = ei.first; edge_iter != ei.second; ++edge_iter) {
        std::cout << "(" << source(*edge_iter, this->graph) << ", " << target(*edge_iter, this->graph) << ")\n";
    }
	std::cout << "-----------------------------\n";
}

PYBIND11_MODULE(boost_graph, m) {
    m.doc() = "pybind11 boost_graph plugin"; // optional module docstring

    py::class_<Graph>(m, "Graph")
    	.def(py::init<>())
    	.def_property("isoLabel", &Graph::getIsoLabel, &Graph::setIsoLabel)
    	.def("add_node", &Graph::add_node)
    	.def("add_edge", &Graph::add_edge)
    	.def("has_node", &Graph::has_node)
    	.def("has_neighbor", &Graph::has_neighbor)
    	.def("printG", &Graph::printG)
	;
}
