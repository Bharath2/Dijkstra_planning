import numpy as np
import heapq as hq
from nodeclass import Node
from maputils import *
from time import time

class Dijkstra:
    def __init__(self, map, start_pos):
        ''' Initialise with environment map and start position
        '''
        self.map = map                             # environment map
        self.start_node = map.get_node(start_pos)  # create start node
        self.start_node.cost = 0                   # set the cost of start_node as 0
        self.explored = {start_pos: 0}             # initialise the explored nodes dict
        # variable to store recently explored path
        self.recent_path = None
        
    def search(self, goal_pos):
        ''' Search for a path from start to given goal position
        '''
        # initialise heap with start node
        heap = [self.start_node]
        # Run Dijkstra Algorithm
        start_t = time()
        while heap:
            curr_node = hq.heappop(heap)  # pop the next node in heap
            self.map.close(curr_node.pos) # close the poped node
            # if the curr_node is goal return path
            if curr_node.pos == goal_pos:
                end_t = time()
                print('\nPath found in', np.round(end_t - start_t, 3), 'seconds\n')
                print('Cost from start to goal: ', np.round(curr_node.cost, 3))
                return self.backtrack(curr_node)
            # get all children of the  current node
            for new_pos, new_cost in curr_node.children():
                # if the new position is not open, skip the below steps
                if self.map.is_open(new_pos):
                    child_node = self.map.get_node(new_pos)
                    # update the cost if required
                    if new_cost < child_node.cost:
                        child_node.cost = new_cost 
                        child_node.parent = curr_node
                        # update the heap with new cost
                        if new_pos not in self.explored: 
                            hq.heappush(heap, child_node)
                        else: hq.heapify(heap)  
                        # update the explored dict
                        self.explored[new_pos] = new_cost
        # if the heap is exhausted, path is not found. 
        print('Goal is not reachable')
        return None
        
        
    def backtrack(self, node):
        ''' Backtrack the path from given node to start node
        '''
        path = []
        while node.parent is not None:
            path.append(node)
            node = node.parent
        path.reverse()
        self.recent_path = path
        return path
    
    
    def visualize(self, path, name = 'result'):
        ''' Visualise the exploration and the recently found path
        '''
        img = self.map.get_image()
        h, w, _ = img.shape
        # open video writer
        out = cv2.VideoWriter(f'{name}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60.0, (w, h))
        # visualize exploration
        k = 0
        for pos, cost in self.explored.items():
            pos = 249 - pos[1], pos[0]
            img[pos] = [255 - int(255/620*cost)]*2 + [0]
            if k%200 == 0:
                out.write(img)
                cv2.imshow('Exploration', img)
                cv2.waitKey(1)
            k += 1
            
        # visualise path
        for node in self.recent_path:
            pos = node.pos
            img[249 - pos[1], pos[0]] = [51, 87, 255]
        for i in range(100): out.write(img)
            
        #show final image and save video
        cv2.imshow('Exploration', img)
        cv2.imwrite('final.jpg', img)
        print('\npress any key to exit')
        cv2.waitKey(0)
        out.release()
        print(f'Video saved as {name}.mp4')
            