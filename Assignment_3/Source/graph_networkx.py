import random

import numpy as np
import networkx as nx
import networkx.drawing
import matplotlib.pyplot as mt

n = int(input('enter n:'))

distances = [[0 for i in range(n)] for j in range(n)]
G = nx.Graph()

for i in range(0, n):
    G.add_node(i)
    for j in range(0, n):
        if (i >= j):
            distances[i][j] = distances[j][i]

        elif (i < j):
            d = random.randint(1, 50)
            distances[i][j] = d
            G.add_edge(i, j, weight=d)

for i in distances:
    print(i)

print(G.number_of_nodes())

labels = nx.get_edge_attributes(G, 'weight')

print(labels)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

mt.show()
