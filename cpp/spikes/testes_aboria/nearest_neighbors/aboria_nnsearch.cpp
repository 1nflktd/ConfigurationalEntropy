#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <Aboria.h>

#include <vector>
#include <tuple>
#include <set>
#include <iostream>
#include <cmath>

namespace py = pybind11;

/*
g++ -O3 -Wall -shared -std=c++14 -I../../testes_pybind11/pybind11/include -I../Aboria/src -I../Aboria/third-party -fPIC `python-config --includes` aboria_nnsearch.cpp -o aboria_nnsearch.so
cp aboria_nnsearch.so ../../testes_pybind11/boost_graph/
*/

template<typename T>
using Vector = std::vector<T>;

template<typename T>
using Vector2D = std::vector<Vector<T>>;

using Particle_t = Aboria::Particles<std::tuple<>, 3, std::vector, Aboria::Kdtree>;
using Particle_position = Particle_t::position;

struct SearchTree {

	SearchTree(int nDimensions, int nParticles, bool pbcX, bool pbcY, bool pbcZ) :
		_nDimensions(nDimensions), _nParticles(nParticles), _pbcX(pbcX), _pbcY(pbcY), _pbcZ(pbcZ), _largestRadius(0), _particles(nParticles) {}

	void add_positions(const py::array_t<double> & positions);
	void init_search(double xMin, double xMax, double yMin, double yMax, double zMin, double zMax);
	py::list search_nearest_neighbors(double x, double y, double z, unsigned int n);

private:
	int _nDimensions;
	int _nParticles;
	bool _pbcX;
	bool _pbcY;
	bool _pbcZ;
	int _largestRadius;
	Particle_t _particles;
	// todo: create cache
};

void SearchTree::add_positions(const py::array_t<double> & positions) {
	auto rows = positions.unchecked<2>();

	for (int i = 0; i < _nParticles; ++i) {
		//if (_nDimensions == 3) {}
		Aboria::get<Particle_position>(_particles)[i] = Aboria::vdouble3(rows(i, 0), rows(i, 1), rows(i, 2));
	}
}

void SearchTree::init_search(double xMin, double xMax, double yMin, double yMax, double zMin, double zMax) {
	Aboria::vdouble3 min = Aboria::vdouble3(xMin, yMin, zMin);
	Aboria::vdouble3 max = Aboria::vdouble3(xMax, yMax, zMax);
	Aboria::vbool3 periodic = Aboria::vbool3(_pbcX, _pbcY, _pbcZ);
	_largestRadius = std::ceil((min - max).norm());
	_particles.init_neighbour_search(min, max, periodic);
}

py::list SearchTree::search_nearest_neighbors(double x, double y, double z, unsigned int n) {
	using Pair = std::pair<double, int>;
	std::set<Pair> distNeighbors;
	std::unordered_set<int> uniqueNeighbors;

	double radius = 3; // optimize this value?
	int maxRadius = 5;
	do {
		for (auto i = Aboria::euclidean_search(_particles.get_query(), Aboria::vdouble3(x, y, z), radius); i != false; ++i) {
			auto inserted = distNeighbors.emplace(Pair{(i.dx()).norm(), Aboria::get<Aboria::id>(*i)});
			if (inserted.second) {
				uniqueNeighbors.emplace(inserted.first->second);
			}
		}

		if (radius >= maxRadius && uniqueNeighbors.size() < n) {
			maxRadius += 1;
		}

		radius += 1;
	} while (radius <= maxRadius && radius <= _largestRadius);

	py::list neighbors;
	std::set<int> alreadyReturned;
	for (const auto & neighbor : distNeighbors) {
		auto inserted = alreadyReturned.emplace(neighbor.second);
		if (inserted.second) {
			neighbors.append(neighbor.second);
			if (alreadyReturned.size() >= n) {
				break;
			}
		}
	}

	return neighbors;
}

PYBIND11_MODULE(aboria_nnsearch, m) {
	m.doc() = "pybind11 aboria_nnsearch plugin";

	py::class_<SearchTree, std::shared_ptr<SearchTree>>(m, "SearchTree")
		.def(py::init<int, int, bool, bool, bool>())
		.def("add_positions", &SearchTree::add_positions)
		.def("init_search", &SearchTree::init_search)
		.def("search_nearest_neighbors", &SearchTree::search_nearest_neighbors)
	;

}
