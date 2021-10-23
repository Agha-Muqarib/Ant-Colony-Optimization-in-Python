#!/usr/bin/env python
# coding: utf-8

# #                             Ant Colony Optimization in Python

# In[31]:


pip install ACO-pants


# In[1]:


import random as rn
import numpy as np
from numpy.random import choice

class AntColony(object):

    def __init__(self, distances, ants, best, iterations, decay, alpha=5, beta=5):
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.ants = ants
        self.best = best
        self.iterations = iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        globalShortestPath = ("Placeholder", np.inf)
        
        for i in range(self.iterations):
            all_paths = self.allPaths()
            self.dropPheromone(all_paths, self.best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print (shortest_path)
            if shortest_path[1] < globalShortestPath[1]:
                globalShortestPath = shortest_path            
            self.pheromone = self.pheromone * self.decay            
        return globalShortestPath

    def dropPheromone(self, all_paths, best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def pathDistance(self, path):
        totalDistance = 0
        for q in path:
            totalDistance += self.distances[q]
        return totalDistance

    def allPaths(self):
        all_paths = []
        for i in range(self.ants):
            path = self.generatePaths(0)
            all_paths.append((path, self.pathDistance(path)))
        return all_paths

    def generatePaths(self, start):
        path = []
        visited = set()
        visited.add(start)
        previous = start
        for i in range(len(self.distances) - 1):
            move = self.pickMove(self.pheromone[previous], self.distances[previous], visited)
            path.append((previous, move))
            previous = move
            visited.add(move)
        path.append((previous, start))   
        return path

    def pickMove(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        normalRow = row / row.sum()
        move = choice(self.all_inds, 1, p=normalRow)[0]
        return move

# Driver Code

distance = np.array([[np.inf, 1, 2, 3, 4],
                      [5, np.inf, 6, 7, 8],
                      [9, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

print("\nAll Iterations : \n")
ob1 = AntColony(distance, 1, 0, 20, 0.7, alpha=5, beta=5)
sPath = ob1.run()

print ("\nShortest Path = ", sPath)

