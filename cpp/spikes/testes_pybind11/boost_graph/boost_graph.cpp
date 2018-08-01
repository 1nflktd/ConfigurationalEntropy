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

python2 main_boost.py ../../../../python/graph_files/fcc.xyz 1.12 0 3 10
python2 -m cProfile -s time main_boost.py ../../../../python/graph_files/fcc.xyz 1.12 0 3 10
python2 -m cProfile -s time main.py graph_files/fcc.xyz 1.12 0 3 10
python2 -m cProfile -s time main.py graph_files/fcc.xyz 1.12 0 3 15
*/

using Edge = std::pair<int, int>;
using Vertex = int;
using UndirectedGraph = boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, Vertex, Edge>;
using edge_iterator = boost::graph_traits<UndirectedGraph>::edge_iterator;
using vertex_iterator = boost::graph_traits<UndirectedGraph>::vertex_iterator;
using vertex_descriptor = boost::graph_traits<UndirectedGraph>::vertex_descriptor;
using adjacency_iterator = boost::graph_traits<UndirectedGraph>::adjacency_iterator;

struct Graph {
	Graph() : isoLabel(0), graph(std::make_shared<UndirectedGraph>()) {}

	inline std::shared_ptr<UndirectedGraph> getGraph() const { return graph; }
	inline int get_iso_label() const { return isoLabel; }
	inline void set_iso_label(int _isoLabel) { isoLabel = _isoLabel; }
	void add_node(int node);
	void add_edge(int e1, int e2);
	bool has_node(int node);
	py::list get_neighbors(int node);
	bool has_neighbor(int node, int neighbor);
	int get_total_nodes();
	int get_total_edges();
	void print_graph();

	int isoLabel;
private:
	std::shared_ptr<UndirectedGraph> graph;
	std::map<int, vertex_descriptor> mVertexDesc;
};

void Graph::add_node(int node) {
	// std::cout << "add_node\n" << node << "\n";

	vertex_descriptor v = boost::add_vertex(node, *this->graph);
	mVertexDesc[node] = v;
}

void Graph::add_edge(int e1, int e2) {
	// if vertices not present, add
	if (mVertexDesc.find(e1) == mVertexDesc.end()) { this->add_node(e1); }
	if (mVertexDesc.find(e2) == mVertexDesc.end()) { this->add_node(e2); }

	// std::cout << "add_edge\n" << e1 << " " << e2 << "\n";
	boost::add_edge(mVertexDesc[e1], mVertexDesc[e2], *this->graph);
}

bool Graph::has_node(int node) {
	// std::cout << "has_node\n" << node << "\n";

	return mVertexDesc.find(node) != mVertexDesc.end();
}

bool Graph::has_neighbor(int node, int neighbor) {
	// std::cout << "has_neighbor\n" << node << " " << neighbor << "\n";

	if (mVertexDesc.find(node) == mVertexDesc.end()) { return false; }
	if (mVertexDesc.find(neighbor) == mVertexDesc.end()) { return false; }

	return boost::edge(mVertexDesc[node], mVertexDesc[neighbor], *this->graph).second;
}

py::list Graph::get_neighbors(int node) {
	py::list neighbors;

	// std::cout << "get_neighbors\n" << node << "\n";

	if (mVertexDesc.find(node) == mVertexDesc.end()) { return neighbors; }

	adjacency_iterator neighbor, neighbor_end;
	for (tie(neighbor, neighbor_end) = boost::adjacent_vertices(mVertexDesc[node], *this->graph); neighbor != neighbor_end; ++neighbor) {
		neighbors.append((*this->graph)[*neighbor]);
	}

	return neighbors;
}

int Graph::get_total_nodes() {
	return boost::num_vertices(*this->graph);
}

int Graph::get_total_edges() {
	return boost::num_edges(*this->graph);
}

void Graph::print_graph() {
	// std::cout << "print2\n";
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
		vertex_descriptor vs = boost::source(*edge_iter, *this->graph);
		vertex_descriptor vt = boost::target(*edge_iter, *this->graph);
		std::cout << "(" << (*this->graph)[vs] << ", " << (*this->graph)[vt] << ")\n";
	}

	std::cout << "-----------------------------\n";
}

template <typename Graph1, typename Graph2>
struct vf2_callback {

	vf2_callback(const Graph1 & graph1, const Graph2 & graph2) {}
	vf2_callback(Graph1 && graph1, Graph2 && graph2) {}

	template <typename CorrespondenceMap1To2, typename CorrespondenceMap2To1>
	bool operator()(CorrespondenceMap1To2, CorrespondenceMap2To1) const {
		// return on the first mapping found
		return false;
	}
};

bool is_isomorphic(const Graph & graph1, const Graph & graph2) {
	vf2_callback<UndirectedGraph, UndirectedGraph> callback(*graph1.getGraph(), *graph2.getGraph());

	bool is_iso = vf2_subgraph_iso(*graph1.getGraph(), *graph2.getGraph(), callback);
	//std::cout << "is_iso: " << is_iso << "\n";

	return is_iso;
}

double calcShannonEntropy(double Hn, double fi, double m) {
	double pi = fi / m;
	Hn -= (pi * log(pi));
	return Hn;
}

py::tuple check_isomorfism(py::list & graphs, double n, double m, double c) {
	std::map<int, int> label_total;
	int iso_label = 1;

	int size = graphs.size();
	for (int i = 0; i < size; ++i) {
		for (int j = i + 1; j < size; ++j) {
			Graph & graph_i = graphs[i].cast<Graph &>();
			Graph & graph_j = graphs[j].cast<Graph &>();

			int iso_label_i = graph_i.get_iso_label();
			int iso_label_j = graph_j.get_iso_label();

			if (iso_label_i == 0 || iso_label_j == 0) {
				if (is_isomorphic(graph_i, graph_j)) {
					if (iso_label_i == 0 && iso_label_j == 0) {
						graph_i.set_iso_label(iso_label);
						graph_j.set_iso_label(iso_label);
						label_total[iso_label] = 2;
						iso_label += 1; // label already used
					} else if (iso_label_i > 0 && iso_label_j == 0) {
						graph_j.set_iso_label(iso_label_i);
						label_total[iso_label_i] += 1;
					} else if (iso_label_j > 0 && iso_label_i == 0) {
						graph_i.set_iso_label(iso_label_j);
						label_total[iso_label_j] += 1;
					} else if (iso_label_i != iso_label_j) {
						std::cout << "Error while checking isomorphism:\nlabelGi " << iso_label_i << " : labelGj " << iso_label_j << "\n";
					}
				}
			}
		}
	}

	// get all graphs that are not isomorphic with any other
	for (const auto & g : graphs) {
		const Graph & g1 = g.cast<const Graph &>();
		if (g1.get_iso_label() == 0) {
			label_total[iso_label] = 1;
			iso_label += 1;
		}
	}

	double H_n = 0.0, H1n = 0.0;
	for (int i = 1; i < iso_label; ++i) {
		double fi = double(label_total[i]);
		H_n = calcShannonEntropy(H_n, fi, m);
		if (fi == 1.0) {
			H1n = calcShannonEntropy(H1n, fi, m);
		}
	}

	double H1nDiv = 0.0;
	if (H_n > 0) {
		H1nDiv = (H1n / H_n);
	}

	double H_n_extrapolated = H_n + (c * H1nDiv);
	double g_n = 2 * log(n); // (spatial_dimensions - 1)
	double Hc_n = H_n_extrapolated - g_n;

	bool valid = true;
	if (H1n > (H_n / 100)) {
		valid = false;
	}

	return py::make_tuple(Hc_n, valid);
}

PYBIND11_MODULE(boost_graph, m) {
	m.doc() = "pybind11 boost_graph plugin"; // optional module docstring

	py::class_<UndirectedGraph, std::shared_ptr<UndirectedGraph>>(m, "UndirectedGraph");

	py::class_<Graph, std::shared_ptr<Graph>>(m, "Graph")
		.def(py::init<>())
		.def_readwrite("isoLabel", &Graph::isoLabel)
		.def("add_node", &Graph::add_node)
		.def("add_edge", &Graph::add_edge)
		.def("has_node", &Graph::has_node)
		.def("has_neighbor", &Graph::has_neighbor)
		.def("get_neighbors", &Graph::get_neighbors)
		.def("get_total_nodes", &Graph::get_total_nodes)
		.def("get_total_edges", &Graph::get_total_edges)
		.def("print_graph", &Graph::print_graph)
	;

	m.def("is_isomorphic", &is_isomorphic);
	m.def("check_isomorfism", &check_isomorfism);
}
