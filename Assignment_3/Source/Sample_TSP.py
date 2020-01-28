import copy
import random

import numpy as np
import networkx as nx
import networkx.drawing
import matplotlib.pyplot as mt

import math
import datetime
import time

import statistics as s


class Ant:

    # constructor
    def __init__(self, state=None, parent=None, visitedCities=[], unVisitedCities=[]):
        self.state = state
        self.parent = None
        self.path_cost = 0
        self.children = None
        self.unVisitedCities = []
        self.visitedCities = []
        self.tourLength = 0
        self.initialCity = None

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setPathCost(self, path_cost):
        self.path_cost = path_cost

    def getPathCost(self):
        return self.path_cost

    def setChildren(self, children):
        self.children = children

    def getChildren(self):
        return self.children

    def setUnVisitedCities(self, unVisitedCities):
        self.unVisitedCities = unVisitedCities

    def getUnVisitedCities(self):
        return self.unVisitedCities

    def setVisitedCities(self, visitedCities):
        self.visitedCities = visitedCities

    def getVisitedCities(self):
        return self.visitedCities

    def setTourLength(self, tourLength):
        self.tourLength = tourLength

    def getTourLength(self):
        return self.tourLength

    def setInitialCity(self, initialCity):
        self.initialCity = initialCity

    def getInitialCity(self):
        return self.initialCity


# -------------------------------------------------------------


def chooseCity(ant):
    start = ant.getVisitedCities()[len(ant.getVisitedCities()) - 1]

    denominator = 0
    cityCount = 0
    for i in ant.getUnVisitedCities():
        T = ((pheromonesTrail[start][i]) ** alpha)
        C = (1 / cities[start][i]) ** beta
        denominator += (T * C)

    maxCity = -1
    max = -1

    for i in ant.getUnVisitedCities():

        # print('city:', (T*C))
        T = ((pheromonesTrail[start][i]) ** alpha)
        C = (1 / cities[start][i]) ** beta
        prob = ((T * C) / denominator)

        if (prob > max):
            max = prob
            maxCity = i

    return maxCity


def updatePheromoneLevelsOnEdges(antsList):
    deltaT = 0

    for i in range(0, len(pheromonesTrail)):
        for j in range(0, len(pheromonesTrail)):
            if (i >= j):
                pheromonesTrail[i][j] = pheromonesTrail[j][i]
            else:
                counter = 0
                for k in antsList:
                    for t in range(0, len(k.getVisitedCities()) - 1):
                        if ((k.getVisitedCities()[t] == i and k.getVisitedCities()[t + 1] == j) or (
                                k.getVisitedCities()[t] == j and k.getVisitedCities()[t + 1] == i)):
                            deltaT += (Q / k.getTourLength())

                    counter += 1

                pheromonesTrail[i][j] = (1 - rho) * (pheromonesTrail[i][j]) + deltaT
                deltaT = 0


def display(antsList):
    for k in antsList:
        print('InitialCity:', k.getInitialCity())
        print('visited:', k.getVisitedCities())
        print('unvisited:', k.getUnVisitedCities())
        print('------------------------------------')


def ACO(maxIterations, antsList):
    meanLength = []
    sLength = []

    for i in antsList:
        print(i.getInitialCity(), end=' ')
    print()

    for i in antsList:
        for j in range(0, n):
            if (i.getInitialCity() == j):
                i.getVisitedCities().append(j)
            else:
                i.getUnVisitedCities().append(j)

    display(antsList)

    shorterTourLength = float('inf')
    shorterTour = []
    for t in range(0, maxIterations):

        tGraph = nx.Graph()

        for x in range(0, n):
            tGraph.add_node(x)

        print('maxIteration:', t)
        if (t != 0):
            for i in antsList:
                i.getVisitedCities().clear()
                i.getUnVisitedCities().clear()
                for j in range(0, n):
                    if (i.getInitialCity() == j):
                        i.getVisitedCities().append(j)
                    else:
                        i.getUnVisitedCities().append(j)

        edgeweights = [[0.1 for i in range(n)] for j in range(n)]
        for k in antsList:

            for j in range(0, n - 1):
                city = chooseCity(k)
                k.getVisitedCities().append(city)
                k.getUnVisitedCities().remove(city)

            k.getVisitedCities().append(k.getInitialCity())

            L = 0
            for j in range(0, len(k.getVisitedCities()) - 1):
                L += cities[k.getVisitedCities()[j]][k.getVisitedCities()[j + 1]]
            k.setTourLength(L)

            for y in range(0, len(k.getVisitedCities()) - 1):
                start = k.getVisitedCities()[y]
                end = k.getVisitedCities()[y + 1]
                edgeweights[start][end] += 0.05

        for i in range(0, n):
            for j in range(0, n):
                tGraph.add_edge(i, j, weight=edgeweights[i][j])

        # tGraph.add_edge(k.getVisitedCities()[y], k.getVisitedCities()[y + 1], weight=2)
        edges = tGraph.edges()
        weights = [tGraph[u][v]['weight'] for u, v in edges]
        # mt.figure('Input 1')
        # mt.title('iteration ' + str(t + 1))
        # nx.draw(tGraph, with_labels=True, width=weights)
        # mt.show()
        print('\n')

        # for k in antsList:
        #     print(k.getVisitedCities(), ' -->TourLength:', k.getTourLength())

        for k in antsList:
            if (k.getTourLength() <= shorterTourLength):
                shorterTourLength = k.getTourLength()
                shorterTour = copy.deepcopy(k.getVisitedCities())

        updatePheromoneLevelsOnEdges(antsList)

        # print('shorter length:', shorterTourLength)
        # print('shorter Tour:', shorterTour)

        tempLength = []
        for m in antsList:
            tempLength.append(m.getTourLength())

        meanLength.append(s.mean(tempLength))
        sLength.append(shorterTourLength)

        flag = False
        for m in antsList:
            if (shorterTourLength != m.getTourLength()):
                flag = True
                break
        if (not flag):
            print('\n\nconverged')
            return shorterTourLength, shorterTour

    return shorterTourLength, shorterTour, meanLength, sLength


n = int(input('enter n:'))
ants = int(input('enter #ants >= n:'))
maxIterations = 50
alpha = 0.7
beta = 0.7
rho = 0.5
Q = 1

cities = [[0 for i in range(n)] for j in range(n)]
pheromonesTrail = [[1 for i in range(n)] for j in range(n)]

for i in range(0, n):
    pheromonesTrail[i][i] = 0

for i in range(0, n):
    for j in range(0, n):
        if (i >= j):
            cities[i][j] = cities[j][i]
        elif (i < j):
            d = random.randint(1, 50)
            cities[i][j] = d

cities = [
    [0, 49, 22, 8, 26, 37, 3, 31, 22, 4, 45, 33, 35, 35, 8, 12, 31, 43, 48, 47, 1, 46, 34, 28, 13, 35, 45, 1, 43, 37],
    [49, 0, 30, 18, 40, 15, 31, 38, 40, 8, 35, 30, 38, 46, 47, 34, 45, 24, 6, 49, 49, 31, 40, 27, 8, 7, 24, 42, 13, 50],
    [22, 30, 0, 5, 45, 12, 11, 46, 19, 31, 26, 36, 49, 23, 12, 41, 39, 25, 19, 50, 27, 34, 30, 36, 23, 28, 6, 16, 4,
     22],
    [8, 18, 5, 0, 4, 38, 29, 27, 12, 8, 33, 44, 46, 2, 33, 17, 8, 20, 38, 23, 43, 49, 47, 39, 15, 33, 21, 40, 50, 31],
    [26, 40, 45, 4, 0, 38, 1, 17, 35, 46, 7, 33, 13, 46, 8, 5, 29, 15, 9, 41, 6, 27, 14, 23, 32, 29, 48, 26, 9, 7],
    [37, 15, 12, 38, 38, 0, 45, 35, 20, 23, 34, 14, 14, 12, 38, 44, 19, 48, 23, 7, 18, 28, 31, 14, 45, 34, 31, 29, 40,
     8],
    [3, 31, 11, 29, 1, 45, 0, 43, 19, 22, 16, 13, 24, 3, 26, 9, 24, 44, 21, 7, 37, 11, 1, 40, 47, 9, 14, 3, 31, 15],
    [31, 38, 46, 27, 17, 35, 43, 0, 48, 26, 2, 12, 21, 4, 21, 47, 38, 48, 31, 33, 38, 3, 19, 15, 33, 4, 35, 10, 28, 50],
    [22, 40, 19, 12, 35, 20, 19, 48, 0, 15, 34, 44, 10, 50, 16, 48, 45, 11, 22, 17, 47, 21, 39, 19, 37, 41, 16, 11, 31,
     38],
    [4, 8, 31, 8, 46, 23, 22, 26, 15, 0, 29, 40, 21, 43, 30, 46, 24, 23, 49, 2, 17, 13, 35, 39, 30, 8, 35, 48, 25, 50],
    [45, 35, 26, 33, 7, 34, 16, 2, 34, 29, 0, 42, 16, 50, 45, 42, 10, 17, 23, 50, 26, 34, 49, 40, 12, 43, 34, 24, 32,
     1],
    [33, 30, 36, 44, 33, 14, 13, 12, 44, 40, 42, 0, 15, 37, 49, 24, 42, 41, 18, 47, 47, 8, 1, 36, 49, 47, 7, 1, 40, 18],
    [35, 38, 49, 46, 13, 14, 24, 21, 10, 21, 16, 15, 0, 31, 41, 4, 2, 30, 2, 30, 49, 48, 38, 34, 30, 38, 12, 45, 46, 3],
    [35, 46, 23, 2, 46, 12, 3, 4, 50, 43, 50, 37, 31, 0, 27, 22, 4, 28, 10, 7, 14, 2, 17, 4, 37, 1, 34, 26, 43, 31],
    [8, 47, 12, 33, 8, 38, 26, 21, 16, 30, 45, 49, 41, 27, 0, 45, 18, 33, 25, 28, 48, 46, 36, 39, 39, 33, 45, 18, 5, 2],
    [12, 34, 41, 17, 5, 44, 9, 47, 48, 46, 42, 24, 4, 22, 45, 0, 38, 33, 29, 42, 42, 44, 2, 34, 25, 33, 41, 13, 26, 31],
    [31, 45, 39, 8, 29, 19, 24, 38, 45, 24, 10, 42, 2, 4, 18, 38, 0, 20, 22, 24, 6, 18, 41, 7, 11, 26, 9, 41, 34, 47],
    [43, 24, 25, 20, 15, 48, 44, 48, 11, 23, 17, 41, 30, 28, 33, 33, 20, 0, 23, 28, 41, 30, 25, 26, 34, 24, 18, 1, 24,
     47],
    [48, 6, 19, 38, 9, 23, 21, 31, 22, 49, 23, 18, 2, 10, 25, 29, 22, 23, 0, 28, 21, 38, 37, 21, 18, 13, 40, 8, 46, 31],
    [47, 49, 50, 23, 41, 7, 7, 33, 17, 2, 50, 47, 30, 7, 28, 42, 24, 28, 28, 0, 9, 15, 45, 6, 44, 28, 41, 47, 42, 7],
    [1, 49, 27, 43, 6, 18, 37, 38, 47, 17, 26, 47, 49, 14, 48, 42, 6, 41, 21, 9, 0, 49, 25, 14, 39, 15, 39, 26, 35, 25],
    [46, 31, 34, 49, 27, 28, 11, 3, 21, 13, 34, 8, 48, 2, 46, 44, 18, 30, 38, 15, 49, 0, 25, 3, 48, 4, 44, 28, 49, 7],
    [34, 40, 30, 47, 14, 31, 1, 19, 39, 35, 49, 1, 38, 17, 36, 2, 41, 25, 37, 45, 25, 25, 0, 2, 49, 27, 30, 30, 48, 23],
    [28, 27, 36, 39, 23, 14, 40, 15, 19, 39, 40, 36, 34, 4, 39, 34, 7, 26, 21, 6, 14, 3, 2, 0, 36, 31, 29, 34, 27, 3],
    [13, 8, 23, 15, 32, 45, 47, 33, 37, 30, 12, 49, 30, 37, 39, 25, 11, 34, 18, 44, 39, 48, 49, 36, 0, 36, 42, 26, 46,
     27],
    [35, 7, 28, 33, 29, 34, 9, 4, 41, 8, 43, 47, 38, 1, 33, 33, 26, 24, 13, 28, 15, 4, 27, 31, 36, 0, 24, 40, 39, 39],
    [45, 24, 6, 21, 48, 31, 14, 35, 16, 35, 34, 7, 12, 34, 45, 41, 9, 18, 40, 41, 39, 44, 30, 29, 42, 24, 0, 41, 10,
     30],
    [1, 42, 16, 40, 26, 29, 3, 10, 11, 48, 24, 1, 45, 26, 18, 13, 41, 1, 8, 47, 26, 28, 30, 34, 26, 40, 41, 0, 34, 30],
    [43, 13, 4, 50, 9, 40, 31, 28, 31, 25, 32, 40, 46, 43, 5, 26, 34, 24, 46, 42, 35, 49, 48, 27, 46, 39, 10, 34, 0,
     38],
    [37, 50, 22, 31, 7, 8, 15, 50, 38, 50, 1, 18, 3, 31, 2, 31, 47, 47, 31, 7, 25, 7, 23, 3, 27, 39, 30, 30, 38, 0]
]  # hardcore

# graph
G = nx.Graph()

for i in range(0, n):
    G.add_node(i)
    for j in range(0, n):
        if (i < j):
            G.add_edge(i, j, weight=cities[i][j])

print(G.number_of_nodes())
labels = nx.get_edge_attributes(G, 'weight')
print(labels)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
mt.show()

antsList = []

# ----------------------------------------------------------------------------------------------

for i in range(0, ants):  # random assignment of cities to ants
    a = Ant()
    r = random.randint(0, n - 1)
    a.setInitialCity(r)
    antsList.append(a)

# initial = [9, 4, 5, 1, 3, 5, 8, 3, 2, 9]  # fixed assignment of cities to ants
# for i in range(0, ants):
#     a = Ant()
#     a.setInitialCity(initial[i])
#     antsList.append(a)

# for i in range(0, ants):  # sequential assignment of cities to ants
#     a = Ant()
#     a.setInitialCity(i % n)
#     antsList.append(a)

# ------------------------------------------------------------------------------------

# ---------------------------Printing Initial-----------------------------------------
print('Initial Cities:')
for i in antsList:
    print(i.getInitialCity(), end=' ')

print('\nCities:')
for i in cities:
    print(i)

print('pheromonesTrail:')
for i in pheromonesTrail:
    print(i)
# ------------------------------------------------------------------------------------
print()

start_time = time.time();
print('start_time:', start_time);

shortLength, shortTour, meanTourLength, leng = ACO(maxIterations, antsList)  # calling ACO

print('**************************\n')
print('shorterLength:', shortLength)
print('shortestTour:', shortTour)
print('\n**************************')

print('end time:', time.time());
print(time.time() - start_time);
elapsed_time_secs = time.time() - start_time;
print('%s sec' % datetime.timedelta(seconds=round(elapsed_time_secs)));

print('shortTour:', shortTour)
finalG = nx.Graph()
for i in range(0, len(shortTour) - 1):
    finalG.add_node(shortTour[i])

for i in range(0, len(shortTour) - 1):
    w = cities[shortTour[i]][shortTour[i + 1]]
    finalG.add_edge(shortTour[i], shortTour[i + 1], weight=w)

print(finalG.number_of_nodes())
labels = nx.get_edge_attributes(finalG, 'weight')
print(labels)
pos = nx.spring_layout(finalG)
nx.draw(finalG, pos, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(finalG, pos, edge_labels=labels)
mt.show()
