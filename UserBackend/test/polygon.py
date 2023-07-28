import numpy as np
import math
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

def orderPoints(points):
    listx = [p[0] for p in points]
    listy = [p[1] for p in points]
    start_point = listx[0], listy[0]
    sorted_points = []
    while len(start_point)>0:
        sorted_points.append(start_point)
        x1, y1 = start_point
        dists = {(x2, y2): np.sqrt((x1-x2)**2 + (y1-y2)**2) for x2, y2 in zip(listx, listy)}
        dists = sorted(dists.items(), key=lambda item: item[1])
        for dist in dists:
            if dist[0] not in sorted_points: 
                start_point = dist[0]
                break
            if dist == dists[-1]:
                start_point = ()
                break
    return sorted_points


def checkIfInside(border, target):
    # Create Point objects
    p = Point(target[0], target[1])
    poly = Polygon(border)
    return p.within(poly)

start_lst = [(-0.500000050000005, -0.5), 
             (-0.499999950000005, 0.5), 
             (-0.500000100000005, -1.0), 
             (-0.49999990000000505, 1.0), 
             (0.500000050000005, -0.5), 
             (-1.0000000250000025, -0.5), 
             (1.0000000250000025, -0.5), 
             (0.499999950000005, 0.5), 
             (-0.9999999750000024, 0.5), 
             (0.9999999750000024, 0.5), 
             (0.500000100000005, -1.0), 
             (0.49999990000000505, 1.0), 
             (-1.0, 0.0), (-0.0, -1.0), 
             (0.0, 1.0), (1.0, 0.0), 
             (-0.500000050000005, -0.5)]
listx = [point[0] for point in start_lst]
listy = [point[1] for point in start_lst]

sorted_points = orderPoints(start_lst)
xs = [point[0] for point in sorted_points]
ys = [point[1] for point in sorted_points]
plt.plot(xs,ys)
plt.show()

print(f'(-1, -1) is inside: {checkIfInside(sorted_points, (-1, -1))}' )
print(f'(0, 0) is inside: {checkIfInside(sorted_points, (0, 0))}' )