import numpy as np
from operator import attrgetter
import random

'''
class for each node in the reactor
'''
class Space:
    def __init__(self, spot) -> None:
        self.spot = spot
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.likelihood = 0
        self.neighbors=set()

'''
class for the reactor environment
'''
class Reactor:
    def __init__(self) -> None:
        with open('Thor23-SA74-VERW-Schematic (Classified).txt', 'r') as f:
            self.lines = f.readlines()
            self.rows=len(self.lines)
            self.columns = len(self.lines[0]) - 1
        self.layout = np.zeros([self.rows, self.columns], dtype=np.object_)
        self.spaces=[]
        self.sequence=[]
    
    '''
    creates the base layout: an array of Space objects
    '''
    def create_layout(self):
        for i in range(self.rows):
            line = self.lines[i]
            for j in range(self.columns):
                if line[j] == '_':
                    self.layout[i][j]=Space(spot=1)
                    self.spaces.append(self.layout[i][j])
                elif line[j] == 'X':
                    self.layout[i][j]=Space(spot=0)
    
    '''
    connects each Space to its neighbor
    '''
    def connect_maze(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if j-1>=0 and self.layout[i][j-1].spot==1:
                    self.layout[i][j].left = self.layout[i][j-1]
                    self.layout[i][j].neighbors.add(self.layout[i][j].left)
                else:
                    self.layout[i][j].left = None

                if j+1<=self.columns-1 and self.layout[i][j+1].spot==1:
                    self.layout[i][j].right = self.layout[i][j+1]
                    self.layout[i][j].neighbors.add(self.layout[i][j].right)
                else:
                    self.layout[i][j].right = None

                if i-1>=0 and self.layout[i-1][j].spot==1:
                    self.layout[i][j].up = self.layout[i-1][j]
                    self.layout[i][j].neighbors.add(self.layout[i][j].up)
                else:
                    self.layout[i][j].up = None

                if i+1<=self.rows-1 and self.layout[i+1][j].spot==1:
                    self.layout[i][j].down = self.layout[i+1][j]
                    self.layout[i][j].neighbors.add(self.layout[i][j].down)
                else:
                    self.layout[i][j].down = None

    '''
    initialize the probabilities of '_' to 1/199
    '''
    def probability_initialize(self):
        count=len(self.spaces)
        for i in self.spaces:
            i.likelihood = 1/count        

    '''
    choose the neighbor based on direction
    '''
    def movement(self, position, direction):
        if direction == "up" and position.up:
            return position.up
        if direction == "down" and position.down:
            return position.down
        if direction == "left" and position.left:
            return position.left
        if direction == "right" and position.right:
            return position.right

        return None

    '''
    distribute probabilities based on the direction to move them
    '''
    def probability_distribute(self, direction):
        temp = []
        prob_addup=dict()
        for pos in self.spaces:
            next_pos = self.movement(pos, direction)
            if next_pos == None:
                continue
            prob_addup[next_pos] = pos.likelihood
            if next_pos not in self.spaces:
                temp.append(next_pos)
            pos.likelihood = 0
        self.spaces.extend(temp)
        for node in prob_addup:
            node.likelihood += prob_addup[node]
        l = [x for x in self.spaces if x.likelihood!=0]
        self.spaces = l
        # print([x.likelihood for x in self.spaces])

    '''
    returns the first non-zero min probability node and the first max probability node
    '''
    def get_min_max(self):
        l = sorted(self.spaces, key=attrgetter('likelihood'))
        while True:
            maximum = max(self.spaces, key = attrgetter('likelihood'))
            minimum = l[0]
            if minimum != maximum:
                return minimum, maximum
            else:
                minimum=l[1]
                return minimum, maximum

    def display(self):
        self.create_layout()
        self.connect_maze()