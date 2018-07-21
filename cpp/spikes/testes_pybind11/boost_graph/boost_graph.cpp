#include <pybind11/pybind11.h>

#include <iostream>
#include <memory>
#include <map>

#include "boost/graph/graph_traits.hpp"
#include "boost/graph/adjacency_list.hpp"
#include "boost/graph/vf2_sub_graph_iso.hpp"

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
using vertex_iterator = boost::graph_traits<UndirectedGraph>::vertex_iterator;
using vertex_descriptor = boost::graph_traits<UndirectedGraph>::vertex_descriptor;

struct Graph {
	Graph() : isoLabel(0), graph(std::make_shared<UndirectedGraph>()) {}

	inline void setIsoLabel(int _isoLabel) { isoLabel = _isoLabel; }
	inline int getIsoLabel() const { return isoLabel; }
	inline std::shared_ptr<UndirectedGraph> getGraph() const { return graph; }
	void add_node(int node);
	void add_edge(int e1, int e2);
	bool has_node(int node);
	bool has_neighbor(int node, int neighbor);
	void print();

private:
	int isoLabel;
	std::shared_ptr<UndirectedGraph> graph;
	std::map<int, vertex_descriptor> mVertexDesc;
	std::map<vertex_descriptor, int> mDescVertex;
};

void Graph::add_node(int node) {
	std::cout << "add_node\n" << node << "\n";
	vertex_descriptor v = boost::add_vertex(node, *this->graph);
	mVertexDesc[node] = v;
	mDescVertex[v] = node;
}

void Graph::add_edge(int e1, int e2) {
	// if vertices not present, add
	if (mVertexDesc.find(e1) == mVertexDesc.end()) { this->add_node(e1); }
	if (mVertexDesc.find(e2) == mVertexDesc.end()) { this->add_node(e2); }

	std::cout << "add_edge\n" << e1 << " " << e2 << "\n";
	boost::add_edge(mVertexDesc[e1], mVertexDesc[e2], *this->graph);
}

bool Graph::has_node(int node) {
	std::cout << "has_node\n" << node << "\n";

	return mVertexDesc.find(node) != mVertexDesc.end();
}

bool Graph::has_neighbor(int node, int neighbor) {
	if (mVertexDesc.find(node) == mVertexDesc.end()) { return false; }
	if (mVertexDesc.find(neighbor) == mVertexDesc.end()) { return false; }

	std::cout << "has_neighbor\n" << node << " " << neighbor << "\n";

	return boost::edge(mVertexDesc[node], mVertexDesc[neighbor], *this->graph).second;
}

void Graph::print() {
	std::cout << "-----------------------------\n";
	std::cout << "vertices:\n";
	std::cout << boost::num_vertices(*this->graph) << "\n";
	std::pair<vertex_iterator, vertex_iterator> vi = boost::vertices(*this->graph);
	for (vertex_iterator vertex_iter = vi.first; vertex_iter != vi.second; ++vertex_iter) {
		std::cout << "(" << (*this->graph)[*vertex_iter] << ")\n";
	}

	std::cout << "edges:\n";
	std::cout << boost::num_edges(*this->graph) << "\n";

	std::pair<edge_iterator, edge_iterator> ei = boost::edges(*this->graph);
	for (edge_iterator edge_iter = ei.first; edge_iter != ei.second; ++edge_iter) {
		const auto & vs = boost::source(*edge_iter, *this->graph);
		const auto & vt = boost::target(*edge_iter, *this->graph);
		std::cout << "(" << mDescVertex[vs] << ", " << mDescVertex[vt] << ")\n";
	}
	std::cout << "-----------------------------\n";
}

template <typename Graph1,typename Graph2>
struct vf2_callback {

	vf2_callback(const Graph1& graph1, const Graph2& graph2) : graph1_(graph1), graph2_(graph2) {}

	template <typename CorrespondenceMap1To2, typename CorrespondenceMap2To1>
	bool operator()(CorrespondenceMap1To2, CorrespondenceMap2To1) const {
		// return on the first mapping found
		return false;
	}

private:
	const Graph1& graph1_;
	const Graph2& graph2_;
};

bool is_isomorphic(const Graph & graph1, const Graph & graph2) {
    vf2_callback<UndirectedGraph, UndirectedGraph> callback(*graph1.getGraph(), *graph2.getGraph());

	bool is_iso = vf2_subgraph_iso(*graph1.getGraph(), *graph2.getGraph(), callback);
	std::cout << "is_iso: " << is_iso << "\n";

	return is_iso;
}

PYBIND11_MODULE(boost_graph, m) {
	m.doc() = "pybind11 boost_graph plugin"; // optional module docstring

	py::class_<UndirectedGraph, std::shared_ptr<UndirectedGraph>>(m, "UndirectedGraph");

	py::class_<Graph, std::shared_ptr<Graph>>(m, "Graph")
		.def(py::init<>())
		.def_property("isoLabel", &Graph::getIsoLabel, &Graph::setIsoLabel)
		.def("add_node", &Graph::add_node)
		.def("add_edge", &Graph::add_edge)
		.def("has_node", &Graph::has_node)
		.def("has_neighbor", &Graph::has_neighbor)
		.def("print", &Graph::print)
	;

	m.def("is_isomorphic", &is_isomorphic);
}
