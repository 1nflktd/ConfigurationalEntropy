#include "Aboria.h"

#include <vector>
#include <iostream>
#include <set>
#include <fstream>

using namespace Aboria;

// g++ -Wall -O3 -std=c++14 -I../../Aboria/src -I../../Aboria/third-party nnsearch.cpp -o nnsearch
// ./nnsearch ../../../../../python/graph_files/fcc.xyz 1 1 1

using Pair = std::pair<double, int>;
using particle_t = Particles<std::tuple<>, 3, std::vector, Kdtree>;
using position = particle_t::position;

int main(int argc, char *argv[]) {
	if (argc != 5) {
		std::cerr << "1: Filename; 2: random point x; 3: random point y; 4: random point z.\n";
		return -1;
	}

	std::ifstream file(argv[1], std::ios::binary);
	std::string line;
	int totalAtoms = 0;

	file >> totalAtoms;
	std::getline(file, line); // skip second line
	std::getline(file, line); // skip second line

	particle_t particles(totalAtoms);
	int i = 0;
	double x, y, z; std::string nop;
	while (file >> nop >> x >> y >> z >> nop) {
		get<position>(particles)[i] = vdouble3(x, y, z);
		i++;
	}

	vdouble3 min = vdouble3(0.0, 0.0, 0.0);
	vdouble3 max = vdouble3(5.105310960166873, 8.842657971447274, 12.505406830647296);
	vbool3 periodic = vbool3(true, true, false);

	particles.init_neighbour_search(min, max, periodic);

	vdouble3 rp = vdouble3(std::stod(argv[2]), std::stod(argv[3]), std::stod(argv[4]));

	std::set<Pair> orderedPoints;
	double radius = 3;
	int count = 0;
	for (auto i = euclidean_search(particles.get_query(), rp, radius); i != false; ++i) {
		count++;

		orderedPoints.emplace(Pair{(i.dx()).norm(), get<id>(*i)});

		std::cout << "Found a particle with dx = " << i.dx() << " and id = " << get<id>(*i) << "\n";
	}

	for (const auto & p : orderedPoints) {
		std::cout << p.second << "\t" << p.first << "\n";
	}

	std::cout << "There are " << count << " particles.\n";

	return 0;
}
