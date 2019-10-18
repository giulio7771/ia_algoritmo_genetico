import math
v1 = [3, 5]
v2 = [4, 10]

# distância euclidiana com numpy

import numpy as np
''
def dist_euclidiana(v1, v2):
	v1, v2 = np.array(v1), np.array(v2)
	diff = v1 - v2
	quad_dist = np.dot(diff, diff)
	return math.sqrt(quad_dist)

print('%.2f' % dist_euclidiana_np(v1, v2))