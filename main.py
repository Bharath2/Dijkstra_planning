import numpy as np
from maputils import *
from dijkstra import Dijkstra

map_size = (400, 250)

obstacles =  [Circle(center = (300, 185), radius = 45),
              Polygon(verts = np.array([[235, 80], [235, 120], [200, 140],
                                        [165, 120], [165, 80], [200, 60]], np.int0)),
              Polygon(verts = np.array([[36, 185], [105, 100], [80, 180]], np.int0)),
              Polygon(verts = np.array([[36, 185], [115, 210], [80, 180]], np.int0)),
             ]

map = Map(map_size, obstacles, clearance = 5)
print('\nMap Created')

print('\nEnter Start position coordinates:')
x_s, y_s = input('x,y: ').split(',')
x_s, y_s = int(x_s), int(y_s)

print('\nEnter Goal position coordinates:')
x_g, y_g = input('x,y: ').split(',')
x_g, y_g = int(x_g), int(y_g)

if map.is_open((x_s, y_s)) and map.is_open((x_s, y_s)):
    # initialise dijsktra search with map and a start position
    dijkstra = Dijkstra(map = map, start_pos = (x_s, y_s))
    # search for a path to goal position
    path = dijkstra.search(goal_pos  = (x_g, y_g))
    # visualize and save explored nodes and path
    dijkstra.visualize(path)
else:
    print('Start or Goal is inside obstacle')
