from env import Space, Reactor
from queue import Queue
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from datetime import datetime

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

def visualize(reactor:Reactor):
    disp = np.zeros([reactor.rows, reactor.columns])
    for i in range(reactor.rows):
        for j in range(reactor.columns):
            if reactor.layout[i][j].spot==0:
                disp[i][j] = np.nan
            else:
                disp[i][j] = reactor.layout[i][j].likelihood
    plt.imshow(disp)
    # plt.savefig('viz/' + datetime.utcnow().strftime("%d%H%M%S%f") +'.png')
    # plt.show()

def convergence(reactor:Reactor):
    
    while reactor.layout[0][-1].likelihood<0.999999:
        min_prob, max_prob = reactor.get_min_max()
        # print(min_prob.likelihood, max_prob.likelihood)
        choose_next_move(min_prob, max_prob, reactor)
        # disp = np.zeros([reactor.rows, reactor.columns])
        # for i in range(reactor.rows):
        #     for j in range(reactor.columns):
        #         if reactor.layout[i][j].spot==0:
        #             disp[i][j] = None
        #         else:
        #             disp[i][j] = reactor.layout[i][j].likelihood
        # for i in disp:
        #     print([j for j in i])
        # print()
        print(len(reactor.sequence))
        # visualize(reactor)

def create_gif():
    directory='viz'
    images = os.listdir(directory)
    filtered_images=[file for file in images if file.endswith('.png')]
    with imageio.get_writer(directory+'/'+'viz.gif', mode='I') as writer:
        for filename in filtered_images:
            image = imageio.imread(directory+'/'+filename)
            writer.append_data(image)
        for filename in filtered_images:
            filepath=os.path.join(directory, filename)
            os.remove(filepath)

def main():
    r = Reactor()
    r.display()
    r.probability_initialize()
    convergence(r)
    print(r.sequence, len(r.sequence))
    # create_gif()

if __name__=='__main__':
    main()