import cv2
import numpy as np
from nodeclass import Node
from scipy.signal import convolve2d

class Map:
    ''' A class for environment map
    '''
    def __init__(self, size, obstacles, clearance):
        ''' Creates the required map
        '''
        # size of the map
        self.size = size
        self.grid = self.create_map(size, obstacles)
        self.grid = self.dilation(self.grid, clearance)
        # generate all nodes 
        self.nodes = [[Node((x, y), None, np.inf) for y in range(size[1])] 
                                                  for x in range(size[0])]
        self.nodes = np.array(self.nodes)
    
    @staticmethod
    def create_map(size, obstacles):
        ''' Create a binary occupancy grid given obstacles list
        '''
        # create an empty grid
        grid = np.zeros(size, np.int8)
        # fill the grid with the given obstacles
        xs, ys = np.indices(size)
        for obs in obstacles:
            grid |= obs.get(xs, ys)
        # boundaries of the map
        grid[(-1, 0), :] = 1; grid[:, (-1, 0)] = 1
        return grid
    
    @staticmethod
    def dilation(grid, cl):
        ''' Add circular clearance to the given grid
        '''
        # get a circle filter
        filter = np.zeros((2*cl + 1, 2*cl + 1))
        cv2.circle(filter, (cl, cl), cl, 1, -1)
        # dilate with above filter 
        mp = convolve2d(grid, filter, mode = 'same')
        mp = np.where(mp > 0, 1, 0)
        return mp + grid
              
    def is_open(self, pos):
        ''' Check if the node is in bounds and free of obstacle
        '''
        # inside the map size
        if pos[0] < 0 or pos[1] < 0: 
            return False 
        if pos[0] >= self.size[0] or pos[1] >= self.size[1]: 
            return False 
        # and node is not closed or obstacle
        return self.grid[pos] == 0
    
    def close(self, pos):
        # close a node when it's cost is finalised
        self.grid[pos] = -1
    
    def get_node(self, pos):
        # get node given position
        return self.nodes[pos]
    
    def get_image(self):
        # To visualise the environment map
        img = np.full((*self.size, 3), 255, np.uint8)
        img[np.where(self.grid == 1)] = 0
        img[np.where(self.grid == 2)] = 50
        img = np.rot90(img)
        return img
        

class Polygon:
    ''' Polygon shaped obstacle class
    '''
    def __init__(self, verts):
        self.N = len(verts)
        self.center = np.mean(verts, axis = 0)
        self.verts = np.vstack((verts, verts[0]))
    
    def get(self, xs, ys):
        cx, cy = self.center
        grid = 1
        # for all polygon edges
        for i in range(self.N):
            x1, y1 = self.verts[i]
            x2, y2 = self.verts[i+1]
            s1 = (xs - x1) * (y2 - y1) - (ys - y1) * (x2 - x1)
            s2 = (cx - x1) * (y2 - y1) - (cy - y1) * (x2 - x1)
            #points on the same side of the edge, as polygon's center
            grid &= (s1*s2 >= 0)
        return grid
        

class Circle:
    ''' Circle shaped obstacle class
    '''
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def get(self, xs, ys):
        cx, cy = self.center
        grid = (xs - cx)**2 + (ys - cy)**2 <= self.radius**2
        return grid



if __name__ == '__main__':
    
    obs = [Circle(center = (300, 185), radius = 40),
           Polygon(verts = np.array([[235, 80], [235, 120], [200, 140],
                                     [165, 120], [165, 80], [200, 60]], np.int0)),
           Polygon(verts = np.array([[36, 185], [105, 100], [80, 180]], np.int0)),
           Polygon(verts = np.array([[36, 185], [115, 210], [80, 180]], np.int0)),
           ]

    map = Map((400, 250), obs, 5)
    img = map.get_image()
    cv2.imshow('test_map', img)
    cv2.waitKey(0)
    


    
