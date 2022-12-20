from env import Space, Reactor
from queue import Queue
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from datetime import datetime

'''
BFS
'''
def get_bfs_path(came_from: dict, end_node):
    cur_node = end_node
    path = [cur_node]
    while cur_node != None:
        path.append(came_from[cur_node])
        cur_node = came_from[cur_node]
    return path[:-2]

def bfs(start_node, end_node):
    q = Queue()
    q.put(start_node)
    came_from = dict()
    came_from[start_node] = None

    while not q.empty():
        current_node = q.get()

        if current_node==end_node:
            break
        else:
            pass
        for next in current_node.neighbors:
            if next not in came_from:
                q.put(next)
                came_from[next] = current_node
    
    return get_bfs_path(came_from, current_node)

'''
visualizes the reactor into a png
'''
def visualize(reactor:Reactor):
    disp = np.zeros([reactor.rows, reactor.columns])
    for i in range(reactor.rows):
        for j in range(reactor.columns):
            if reactor.layout[i][j].spot==0:
                disp[i][j] = np.nan
            else:
                disp[i][j] = reactor.layout[i][j].likelihood
    cmap = matplotlib.cm.get_cmap('coolwarm')
    cmap.set_bad('black', 1.)
    plt.imshow(disp, cmap=cmap)
    plt.title(f'Seq. length: {len(reactor.sequence)}, Move: {reactor.sequence[-1]}')
    plt.savefig('viz/' + datetime.utcnow().strftime("%d%H%M%S%f") +'.png')
    plt.show()

'''
displays the reactor in the form of a NumPy array of probabilities
'''
def display_reactor(reactor:Reactor):
    disp = np.zeros([reactor.rows, reactor.columns])
    for i in range(reactor.rows):
        for j in range(reactor.columns):
            if reactor.layout[i][j].spot==0:
                disp[i][j] = None
            else:
                disp[i][j] = reactor.layout[i][j].likelihood
    np.set_printoptions(precision=4)
    for i in disp:
        print([round(j, 4) for j in i]) # rounded to 4 decimal points for visual appeal
    print()

'''
choose the next direction the probabilities shift to based on the BFS path
'''
def choose_next_move(min_prob, max_prob, reactor:Reactor):
    path = bfs(min_prob, max_prob)
    next_node = path[-1]
    if min_prob.left == next_node:
        reactor.sequence.append("left")
        reactor.probability_distribute("left")
    elif min_prob.right == next_node:
        reactor.sequence.append("right")
        reactor.probability_distribute("right")
    elif min_prob.up == next_node:
        reactor.sequence.append("up")
        reactor.probability_distribute("up")
    elif min_prob.down == next_node:
        reactor.sequence.append("down")
        reactor.probability_distribute("down")

'''
converges the probabilities to 1 at a spot
'''
def convergence(reactor:Reactor):
    while reactor.spaces[0].likelihood<0.999999 or len(reactor.spaces)>1:
        min_prob, max_prob = reactor.get_min_max()
        choose_next_move(min_prob, max_prob, reactor)

        # display_reactor(reactor)  # uncomment to print out the probability matrix in the terminal

        print(len(reactor.sequence))

        # visualize(reactor)    # uncomment to save the time frames as pngs

'''
creates a gif out of the pngs
'''
def create_gif(length):
    directory='viz'
    images = os.listdir(directory)
    filtered_images=[file for file in images if file.endswith('.png')]
    with imageio.get_writer(directory+'/viz_'+f'{length}.gif', mode='I') as writer:
        for filename in filtered_images:
            image = imageio.imread(directory+'/'+filename)
            writer.append_data(image)
        for filename in filtered_images:
            filepath=os.path.join(directory, filename)
            os.remove(filepath)

def remove_pngs():
    directory = 'viz'
    images = os.listdir(directory)
    filtered_images=[file for file in images if file.endswith('.png')]
    for filename in filtered_images:
            filepath=os.path.join(directory, filename)
            os.remove(filepath)

def main():
    # for i in range(100):
    r = Reactor()
    r.display()
    r.probability_initialize()
    convergence(r)
    print(r.sequence, len(r.sequence))
    # create_gif(len(r.sequence))

if __name__=='__main__':
    main()