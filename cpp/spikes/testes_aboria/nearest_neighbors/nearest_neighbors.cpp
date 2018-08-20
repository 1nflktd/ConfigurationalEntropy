#include "Aboria.h"

#include <vector>
#include <iostream>
#include <cmath>
#include <set>

using namespace Aboria;

// g++ -Wall -O3 -std=c++14 -I../Aboria/src -I../Aboria/third-party nearest_neighbors.cpp -o nearest_neighbors

double calculateEuclideanDistance(vdouble3 rp, vdouble3 p1) {
	return std::sqrt(
		std::pow(rp[0] - p1[0], 2) +
		std::pow(rp[1] - p1[1], 2) +
		std::pow(rp[2] - p1[2], 2)
	);
}

int main() {

	std::vector<std::vector<double>> points = {
		{0.00000000, 0.00000000, 0.00000000},
		{0.00000000, 1.47377633, 2.08423447},
		{0.00000000, 2.94755266, 4.16846894},
		{1.27632774, 0.73688816, 4.16846894},
		{1.27632774, 2.21066449, -0.00000000},
		{1.27632774, 3.68444082, 2.08423447},
		{2.55265548, -0.00000000, -0.00000000},
		{2.55265548, 1.47377633, 2.08423447},
		{2.55265548, 2.94755266, 4.16846894},
		{3.82898322, 0.73688816, 4.16846894},
		{3.82898322, 2.21066449, -0.00000000},
		{3.82898322, 3.68444082, 2.08423447},
		{0.00000000, 4.42132899, 0.00000000},
		{0.00000000, 5.89510531, 2.08423447},
		{0.00000000, 7.36888164, 4.16846894},
		{1.27632774, 5.15821715, 4.16846894},
		{1.27632774, 6.63199348, -0.00000000},
		{1.27632774, 8.10576981, 2.08423447},
		{2.55265548, 4.42132899, -0.00000000},
		{2.55265548, 5.89510531, 2.08423447},
		{2.55265548, 7.36888164, 4.16846894},
		{3.82898322, 5.15821715, 4.16846894},
		{3.82898322, 6.63199348, -0.00000000},
		{3.82898322, 8.10576981, 2.08423447},
		{0.00000000, 0.00000000, 6.25270342},
		{0.00000000, 1.47377633, 8.33693789},
		{0.00000000, 2.94755266, 10.42117236},
		{1.27632774, 0.73688816, 10.42117236},
		{1.27632774, 2.21066449, 6.25270342},
		{1.27632774, 3.68444082, 8.33693789},
		{2.55265548, 0.00000000, 6.25270342},
		{2.55265548, 1.47377633, 8.33693789},
		{2.55265548, 2.94755266, 10.42117236},
		{3.82898322, 0.73688816, 10.42117236},
		{3.82898322, 2.21066449, 6.25270342},
		{3.82898322, 3.68444082, 8.33693789},
		{0.00000000, 4.42132899, 6.25270342},
		{0.00000000, 5.89510531, 8.33693789},
		{0.00000000, 7.36888164, 10.42117236},
		{1.27632774, 5.15821715, 10.42117236},
		{1.27632774, 6.63199348, 6.25270342},
		{1.27632774, 8.10576981, 8.33693789},
		{2.55265548, 4.42132899, 6.25270342},
		{2.55265548, 5.89510531, 8.33693789},
		{2.55265548, 7.36888164, 10.42117236},
		{3.82898322, 5.15821715, 10.42117236},
		{3.82898322, 6.63199348, 6.25270342},
		{3.82898322, 8.10576981, 8.33693789}
	};

	//ABORIA_VARIABLE(neighbours_count, int, "number of neighbours")

	//typedef Particles<std::tuple<neighbours_count>> particle_t;
	typedef Particles<std::tuple<>, 3, std::vector, Kdtree> particle_t;
	typedef particle_t::position position;

	const size_t N = points.size();
	particle_t particles(N);
	for (size_t i = 0; i < N; ++i) {
		get<position>(particles)[i] = vdouble3(points[i][0], points[i][1], points[i][2]);
	}

	vdouble3 min = vdouble3(0.0, 0.0, 0.0);
	//vdouble3 max = vdouble3(3.92, 8.20, 10.52);
	vdouble3 max = vdouble3(5.105310960166873, 8.842657971447274, 12.505406830647296);
	//vbool3 periodic = vbool3::Constant(true);

	vbool3 periodic = vbool3(true, true, false);
	//vbool3 periodic = vbool3(true, true, true);

	particles.init_neighbour_search(min, max, periodic);

	//vdouble3 rp = vdouble3(0.893079307334, 3.57366629713, 10.2738712726);
	vdouble3 rp = vdouble3(2.893079307334, 1.57366629713, 6.2738712726);

/*
0.893079307334 3.57366629713 10.2738712726
nnPy
[25, 26, 27, 29, 31, 32, 35, 37, 39, 45]
nnAboria
[25, 26, 27, 29, 32, 33, 35, 37, 39, 45]
*/
	using Pair = std::pair<double, int>;

	std::set<Pair> meuSet;
	double radius = 4;
	int count = 0;
	for (auto i = euclidean_search(particles.get_query(), rp, radius); i != false; ++i) {
		count++;

		meuSet.emplace(Pair{(i.dx()).norm(), get<id>(*i)});

		std::cout << "Found a particle with dx = " << i.dx() << " and id = " << get<id>(*i) << "\n";
		//std::cout << (rp - get<position>(*i)).norm() << "\n";
		//std::cout << (rp - i.dx()).norm() << "\n";
		//std::cout << (i.dx()).norm() << "\n";
		//std::cout << "Distance = " << rp - i.dx() << "\n";
		//std::cout << "Euclidean Distance = " << calculateEuclideanDistance(rp, i.dx()) << "\n";
	}

	for (const auto & p : meuSet) {
		std::cout << p.second << "\t" << p.first << "\n";
	}

	std::cout << "There are " << count << " particles.\n";

	return 0;
}
