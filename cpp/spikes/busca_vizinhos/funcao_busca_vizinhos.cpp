#include <vector>
#include <iostream>
#include <map>
#include <algorithm>
#include <random>

template <typename T>
using Vector = std::vector<T>;

template <typename T>
using Matrix = Vector<Vector<T>>;

void printMatrix(const Matrix<int> & g) {
	for (const auto & r : g) {
		for (const auto & c : r) {
			std::cout << c << " ";
		}
		std::cout << "\n";
	}
}

void searchNeighbors(int vertex, int n, int m, const Matrix<int> & graphao, Matrix<int> & graph, Vector<int> & vecPosicoes, int & vizinhosAchados, std::map<int, bool> & verticesVisitados) {
	if (vizinhosAchados >= n) {
		return;
	}

	if (verticesVisitados[vertex]) {
		return;
	}

	auto itVertex = std::find(vecPosicoes.begin(), vecPosicoes.end(), vertex);
	if (itVertex == vecPosicoes.end()) {
		// THROW ERROR ?
		return;
	}

	int posVertex = std::distance(vecPosicoes.begin(), itVertex);
	verticesVisitados[vertex] = true;

	// 1 level
	for (int i = 0; i < graphao[0].size() && vizinhosAchados < n; ++i) {
		if (graphao[vertex][i] == 1) {
			auto itI = std::find(vecPosicoes.begin(), vecPosicoes.end(), i);
			if  (itI == vecPosicoes.end()) {
				++vizinhosAchados;
				// adicionar i no vecposicoes
				// e adicionar posVertex
				vecPosicoes.push_back(i);
				auto posInserted = vecPosicoes.size() - 1;

				graph[posVertex][posInserted] = 1;
				graph[posInserted][posVertex] = 1;
			} else {
				// add graph
				int posI = std::distance(vecPosicoes.begin(), itI);
				graph[posVertex][posI] = 1;
				graph[posI][posVertex] = 1;
			}
		}
	}

	if (vizinhosAchados < n) {
		// achar vizinho nao visitado
		for (const auto & v : vecPosicoes) {
			if (!verticesVisitados[v]) {
				searchNeighbors(v, n, m, graphao, graph, vecPosicoes, vizinhosAchados, verticesVisitados);
			}
		}
	}
}

Vector<Matrix<int>> generateGraphs(int m, int n, const Matrix<int> & graphao) {
	Vector<Matrix<int>> graphs = Vector<Matrix<int>>(m); // m graphs

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, graphao[0].size() - 1); // [0, size]

    Vector<int> verticesGerados(m);

	int nGraph = 0;
	while (nGraph < m) {
		// posicao aleatoria (vertice aleatorio (?))
		int vertex = dis(gen);
		if (std::find(verticesGerados.begin(), verticesGerados.end(), vertex) != verticesGerados.end()) {
			continue;
		}

		verticesGerados.push_back(vertex);
		// achou vertice
		Matrix<int> graph{ Matrix<int>(n + 1, Vector<int>(n + 1, 0)) };
		Vector<int> vecPosicoes; //{ n + 1 }; // ex: 0 -> 101, 1 -> 97, etc.
		//vecPosicoes[0] = vertex;
		vecPosicoes.push_back(vertex);
		std::map<int, bool> verticesVisitados;

		std::cout << "vertex " << vertex << "\n";

		int vizinhosAchados = 0;
		searchNeighbors(vertex, n, m, graphao, graph, vecPosicoes, vizinhosAchados, verticesVisitados);
		graphs[nGraph] = graph;

		std::cout << "grafo\n";
		printMatrix(graph);
		std::cout << "---------------\n";

		++nGraph;
	}

	return graphs;
}

int main() {

	Matrix<int> m1 {
		{0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0},
		{0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1},
		{0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0}
	};

	int m = 12;
	int n = 10;
	Vector<Matrix<int>> graphs = generateGraphs(m, n, m1);

	return 0;
}
