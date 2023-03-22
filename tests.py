import numpy as np

a = np.array([[0, 1, 2],
              [6, 2, 4],
              [0, 3, 6]])

indices = np.where(a == 6)
xmin = indices[0][0]
xmax = indices[0][-1]
ymin = indices[1][0]
ymax = indices[1][-1]


print(f'({xmin}, {ymin}), ({xmax}, {ymax})')