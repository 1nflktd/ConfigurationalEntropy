#include "Aboria.h"

using namespace Aboria;

// g++ -Wall -O3 -std=c++14 -I../Aboria/src -I../Aboria/third-party getting_started.cpp -o getting_started

int main() {
	/*
		* Create a 2d particle container type with one
		* additional variable "velocity", represented
		* by a 2d double vector
	*/

	ABORIA_VARIABLE(velocity, vdouble2, "velocity")
	typedef Particles<std::tuple<velocity>, 2> container_t;
	typedef typename container_t::position position;

	/*
		* create a particle set with size N
	*/
	const int N = 100;
	container_t particles(N);

	std::uniform_real_distribution<double> uni(0, 1);
	std::default_random_engine gen;
	for (int i = 0; i < N; ++i) {
		/*
		* set a random position, and initialise velocity
		*/
		get<position>(particles)[i] = vdouble2(uni(gen), uni(gen));
		get<velocity>(particles)[i] = vdouble2(0, 0);
	}

	/*
	* write particle container to a vtk
	* unstructured grid file
	*/
	//vtkWriteGrid("aboria", 0, particles.get_grid(true));
}
