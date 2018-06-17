import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
import math

def main():
	x = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	gn = [2.772589, 3.218876, 3.583519, 3.891820, 4.158883, 4.394449, 4.605170, 4.795791, 4.969813, 5.129899, 5.278115, 5.416100, 5.545177, 5.666427, 5.780744, 5.888878, 5.991465]

	# m = 3.4 * n * n * N
	hn_1 = [0.671521, 1.088659, 1.504189, 1.509163, 1.935196, 2.147992, 2.683553, 2.885729, 3.147572, 3.308561, 3.270840, 3.431944, 3.674295, 3.737422, 3.715520, 3.743437, 3.577564]
	h1_1 = [0.000000, 0.002623, 0.001904, 0.000000, 0.000000, 0.000928, 0.000000, 0.000000, 0.000000, 0.001441, 0.000841, 0.000371, 0.001322, 0.001184, 0.000000, 0.001210, 0.001985]
	# m = n * n * N
	hn_2 = [0.681959, 1.083765, 1.484341, 1.515710, 1.923200, 2.130017, 2.680858, 2.883819, 3.134245, 3.320725, 3.287065, 3.415805, 3.684789, 3.739381, 3.710328, 3.742596, 3.581849]
	h1_2 = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.002736, 0.004549, 0.003847, 0.000000, 0.000000, 0.005024, 0.001111, 0.000991, 0.003556, 0.003211, 0.003644, 0.003990]
	# m = 3.4 * n * N
	#"""
	hn_3 = [0.687250, 1.063382, 1.485489, 1.406996, 1.889981, 2.125918, 2.686530, 2.859451, 3.187602, 3.313669, 3.258852, 3.402782, 3.641759, 3.716940, 3.710935, 3.729584, 3.561302]
	h1_3 = [0.000000, 0.000000, 0.000000, 0.000000, 0.014066, 0.012717, 0.011617, 0.010703, 0.004965, 0.004633, 0.030418, 0.020467, 0.015482, 0.022031, 0.034939, 0.026666, 0.019125]
	#"""

	c = 0
	y1 = obterY(c, x, h1_1, hn_1, gn)
	y2 = obterY(c, x, h1_2, hn_2, gn)
	y3 = obterY(c, x, h1_3, hn_3, gn)

	c = 1
	y1_2 = obterY(c, x, h1_1, hn_1, gn)
	y2_2 = obterY(c, x, h1_2, hn_2, gn)
	y3_2 = obterY(c, x, h1_3, hn_3, gn)

	c = 2
	y1_3 = obterY(c, x, h1_1, hn_1, gn)
	y2_3 = obterY(c, x, h1_2, hn_2, gn)
	y3_3 = obterY(c, x, h1_3, hn_3, gn)

	x = np.asarray(x)
	y1 = np.asarray(y1)
	y2 = np.asarray(y2)
	y3 = np.asarray(y3)

	y1_2 = np.asarray(y1_2)
	y2_2 = np.asarray(y2_2)
	y3_2 = np.asarray(y3_2)

	y1_3 = np.asarray(y1_3)
	y2_3 = np.asarray(y2_3)
	y3_3 = np.asarray(y3_3)

	# Fit with polyfit
	#b, m = polyfit(x, y, 1)

	#print("Entropia %f" % m)

	font = {'weight': 'bold',
	        'size': 12}

	plt.rc('font', **font)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	axis_font = {'weight': 'bold', 'size':12}

	ax.set_xlabel('n', **axis_font)
	#ax.set_ylabel('H(n) - g(n)', **axis_font)
	ax.set_ylabel('H(n)', **axis_font)

	#ax.plot(x, y, '+')
	ax.plot(x, y1)
	#ax.plot(x, y2)
	#ax.plot(x, y3)

	ax.plot(x, y1_2)
	#ax.plot(x, y2_2)
	#ax.plot(x, y3_2)

	ax.plot(x, y1_3)
	#ax.plot(x, y2_3)
	#ax.plot(x, y3_3)

	#ax.plot(x, b + m * x, '--')
	ax.axis([0, 25, -3, -1.5])

	plt.show()

def obterY(c, x, h1, hn, gn):
	y = []
	i = 0
	for n in x:
		H1nDiv = 0.0
		if hn[i] > 0:
			H1nDiv = (h1[i] / hn[i])

		H_n_extrapolated = hn[i] + (c * H1nDiv)
		hcn = H_n_extrapolated - gn[i]
		#hcn = hn[i] - gn[i]

		y.append(hcn)
		i += 1

	return y

if __name__ == "__main__":
	main()
