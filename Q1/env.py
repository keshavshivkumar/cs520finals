import numpy as np
from operator import attrgetter
import random

class Space:
    def __init__(self, spot) -> None:
        self.spot = spot
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.likelihood = 0
        self.neighbors=set()

class Reactor:
    def __init__(self) -> None:
        with open('Thor23-SA74-VERW-Schematic (Classified).txt', 'r') as f:
            self.lines = f.readlines()
            self.rows=len(self.lines)
            self.columns = len(self.lines[0]) - 1
        self.layout = np.zeros([self.rows, self.columns], dtype=np.object_)
        self.spaces=[]
        self.sequence=[]
    
    def create_layout(self):
        for i in range(self.rows):
            line = self.lines[i]
            for j in range(self.columns):
                if line[j] == '_':
                    self.layout[i][j]=Space(spot=1)
                    if i == 0 and j == self.columns-1:
                        continue
                    self.spaces.append(self.layout[i][j])
                elif line[j] == 'X':
                    self.layout[i][j]=Space(spot=0)
    
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
        self.maximum = self.layout[0][-1]

    def probability_initialize(self):
        count=len(self.spaces)
        for i in self.spaces:
            i.likelihood = 1/count        

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

    def probability_distribute(self, direction):
        temp = []
        prob_addup=dict()
        for pos in self.spaces:
            next_pos = self.movement(pos, direction)
            if next_pos == None:
                continue
            prob_addup[next_pos] = pos.likelihood
            # next_pos.likelihood += pos.likelihood
            if next_pos not in self.spaces and next_pos != self.layout[0][self.columns-1]:
                temp.append(next_pos)
            pos.likelihood = 0
        self.spaces.extend(temp)

        for node in prob_addup:
            node.likelihood+=prob_addup[node]
        # for node in self.spaces:
        #     if node.likelihood == 0:          # does not work
        #         self.spaces.remove(node)
        l = [x for x in self.spaces if x.likelihood!=0]
        self.spaces = l
        # print([x.likelihood for x in self.spaces])

    def get_min_max(self, minimum=None):
        minimum=self.spaces[0]
        temp_min = minimum
        maximum = self.layout[0][-1]
        mini=[minimum]
        for i in self.spaces:
            if i.likelihood < minimum.likelihood:
                minimum=i
                mini=[]
            if i.likelihood == minimum.likelihood:
                mini.append(i)
        while True:
            # print([x.likelihood for x in mini])
            if temp_min.likelihood == mini[0].likelihood:
                random_min = temp_min
            else:
                random_min = random.choice(mini)
            if random_min != maximum:
                return random_min, maximum

    def display(self):
        self.create_layout()
        self.connect_maze()

# def main():
#     r = Reactor()
#     reactor = r.display()
#     for i in reactor:
#         print([j.spot for j in i])