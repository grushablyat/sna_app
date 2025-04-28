from random import random
from typing import Collection
from networkit import vizbridges

import networkit as nk
import numpy as np
import matplotlib.pyplot as plt


nums = {}

def generate_random_graph():
    g = nk.generators.HyperbolicGenerator(1e5).generate()
    communities = nk.community.detectCommunities(g, inspect=True)

    nk.overview(g)
    return g


# Чтение графа
def read_graph(filename: str='graph.graph'):
    # G = nk.readGraph(filename, fileformat=nk.graphio.Format.METIS)
    G = nk.readGraph(filename)

    return G


# Вычисление связных компонент
def linked_components(G):
    cc = nk.components.ConnectedComponents(G)
    cc.run()
    compSizes = cc.getComponentSizes()
    print(f"Число компонент: {len(compSizes)}, размер наибольшей: {max(compSizes.values())}")


def create_n_node_graph(N: int=100):
    G = nk.Graph(n=N)

    for i in range(N):
        for j in range(N):
            if j < i:
                if random() < 0.7:
                    G.addEdge(i, j)

    return G


# Обнаружение сообществ
def detect_communities(G):
    communities = nk.community.PLM(G, refine=True, gamma=1.0, maxIter=32, turbo=False, recurse=True)
    communities.run()
    # print(communities.summary())

    # Визуализация
    sizes = communities.getPartition().subsetSizes()
    sizes.sort(reverse=True)
    plt.plot(sizes)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Community index")
    plt.ylabel("Community size")
    plt.title("Community Size Distribution")
    plt.show()

    return communities


def create_social_graph(friends: Collection, relations: Collection):
    friends = list(friends)
    relations = list(relations)

    G = nk.Graph()
    # G.addEdges(inputData=relations, addMissing=True)

    N = G.addNodes(len(friends))
    fid = G.attachNodeAttribute("fid", int)
    for i in range(len(friends)):
        fid[i] = friends[i].id
        nums[fid[i]] = i

    for relation in relations:
        G.addEdge(nums[relation[0]], nums[relation[1]])

    return G


def user_summary(G, id):
    num = nums[id]
    print(f'ID:      {id}')
    print(f'Degree:  {G.degree(num)}')


# # Don't work (widgets are rendered only in notebooks)
# def visualize(G):
#     btwn = nk.centrality.Betweenness(G)
#     btwn.run()
#
#     nk.vizbridges.widgetFromGraph(G, nodeScores=btwn.scores())
