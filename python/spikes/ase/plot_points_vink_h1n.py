import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
import math

x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
y = []
for n in x:
	y.append( n * 0.2)

#for i in range(13, 18):
#	y[i] = y[i] - 0.5

y[14] = y[14] - 0.1
y[15] = y[15] - 0.2
y[16] = y[16] - 0.35
y[17] = y[17] - 0.5
y[18] = y[18] - 0.65
y[19] = y[19] - 0.8
y[20] = y[20] - 0.9
y[21] = y[21] - 1.05

x = np.asarray(x)
y = np.asarray(y)

# Fit with polyfit
b, m = polyfit(x[:15], y[:15], 1)
#b, m = polyfit(x, y, 1)

print("Entropia %f" % m)

font = {'weight': 'bold',
        'size': 12}

plt.rc('font', **font)

fig = plt.figure()
ax = fig.add_subplot(111)

axis_font = {'weight': 'bold', 'size':12}

ax.set_xlabel('n', **axis_font)
#ax.set_ylabel('H(n) - g(n)', **axis_font)
ax.set_ylabel('H(n) - g(n)', **axis_font)

ax.plot(x, y, '+')
ax.plot(x, b + m * x, '--')
ax.axis([0, 25, 0, 5])

plt.show()
