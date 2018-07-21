//=======================================================================
// Copyright (C) 2012 Flavio De Lorenzi (fdlorenzi@gmail.com)
//
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//=======================================================================

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/vf2_sub_graph_iso.hpp>

using namespace boost;

/*
g++ -O3 -Wall -std=c++14 vf2_sub_graph_iso_example.cpp -o vf2_sub_graph_iso_example
*/

template <typename Graph1,typename Graph2>
struct my_callback {

	my_callback(const Graph1& graph1, const Graph2& graph2) : graph1_(graph1), graph2_(graph2) {}

	template <typename CorrespondenceMap1To2, typename CorrespondenceMap2To1>
	bool operator()(CorrespondenceMap1To2 /*f*/, CorrespondenceMap2To1) const {
		return false;
	}

private:
	const Graph1& graph1_;
	const Graph2& graph2_;
};

int main() {
	typedef adjacency_list<vecS, vecS, undirectedS> graph_type;

	// Build graph1
	int num_vertices1 = 4; graph_type graph1(num_vertices1);
	add_edge(0, 1, graph1);
	add_edge(1, 2, graph1);
	add_edge(2, 3, graph1);

	// Build graph2
	int num_vertices2 = 4; graph_type graph2(num_vertices2);
	add_edge(0, 1, graph2);
	add_edge(0, 2, graph2);
	add_edge(0, 3, graph2);

	// Create callback to print mappings
	//vf2_print_callback<graph_type, graph_type> my_callback(graph1, graph2);
    my_callback<graph_type, graph_type> my_callback(graph1, graph2);

	// Print out all subgraph isomorphism mappings between graph1 and graph2.
	// Vertices and edges are assumed to be always equivalent.
	bool is_iso = vf2_subgraph_iso(graph1, graph2, my_callback);
	std::cout << "is_iso: " << is_iso << "\n";

	return 0;
}
