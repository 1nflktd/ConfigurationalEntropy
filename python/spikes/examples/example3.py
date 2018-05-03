import sys
import networkx as nx
import matplotlib.pyplot as plt

def run(graph, n, m):
	# nx.write_adjlist(graph, sys.stdout)
	# print("%d - %d" % (n, m))
	nx.draw(graph, with_labels=True)
	plt.show()

def main():
	graph = nx.read_adjlist("../../files/graph1.x")
	n = 3
	m = 4
	run(graph, n, m)

if __name__ == "__main__":
	main()