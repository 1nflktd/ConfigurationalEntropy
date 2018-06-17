import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
import math

"""
x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
y = [-2.197361, -2.080489, -2.148112, -1.826753, -2.072123, -2.330320, -2.227933, -2.077688, -2.186206, -1.955939, -2.206133, -2.283686, -2.282529, -2.146971, -2.210375, -2.402572, -2.447510, -2.570687, -2.777405, -2.954710, -2.951758]
"""

x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
y = [-2.197361, -2.080489, -2.148112, -1.926753, -2.072123, -2.330320, -2.227933, -2.077688, -2.086206, -1.855939, -2.106133, -2.183686, -2.182529, -2.106971]

#"""
i = 0
for n in x:
	g_n = 2 * math.log(n)
	y[i] = y[i] + g_n
	i += 1
#"""

x = np.asarray(x)
y = np.asarray(y)

# Fit with polyfit
b, m = polyfit(x, y, 1)

print("Entropia %f" % m)

font = {'weight': 'bold',
        'size': 12}

plt.rc('font', **font)

fig = plt.figure()
ax = fig.add_subplot(111)

axis_font = {'weight': 'bold', 'size':12}

ax.set_xlabel('n', **axis_font)
#ax.set_ylabel('H(n) - g(n)', **axis_font)
ax.set_ylabel('H(n)', **axis_font)

ax.plot(x, y, '+')
ax.plot(x, b + m * x, '--')
ax.axis([0, 18, 0, 5])

plt.show()
