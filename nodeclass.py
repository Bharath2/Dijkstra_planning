import cv2
import numpy as np

action_set = {'U': (( 1, 0), 1), 'UL': (( 1, 1), 1.4),
              'L': (( 0, 1), 1), 'DL': ((-1, 1), 1.4),
              'D': ((-1, 0), 1), 'DR': ((-1,-1), 1.4),
              'R': (( 0,-1), 1), 'UR': (( 1,-1), 1.4), }

class Node:
    ''' Container class for a Node
    ''' 
    def __init__(self, pos, parent, cost):
        ''' Initialise a Node class object
        '''
        self.pos = pos       # Node co-ordinates (tuple: (x, y))
        self.parent = parent # Reference to parent of this node
        self.cost = cost     # cost to come from start node
    
    def __lt__(self, other):
        ''' Compare two nodes based on cost (for min heap)
        '''
        return self.cost < other.cost
        
    def take_action(self, action):
        ''' Returns new position and cost after taking an action 
        '''
        # get the direction to move and cost of the action
        move, cost = action_set[action]
        # add the action step to node position to get new position
        new_pos = (self.pos[0] + move[0], 
                   self.pos[1] + move[1])
        # add the cost of the action to get new cost
        new_cost = self.cost + cost
        return new_pos, new_cost
    
    def children(self):
        ''' A generator of all children of the node
        '''
        for action in action_set.keys():
            yield self.take_action(action)
    
    
    