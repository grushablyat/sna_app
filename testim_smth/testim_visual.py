import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network


def visualize_graph_plt(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.draw(G, with_labels=True)
    plt.show()

def visualize_graph_vis(nodes, edges, filename):
    net = Network(notebook=True)
    net.add_nodes(
        nodes,
        label=[f'{node}' for node in nodes],
        # color=[f'#{hex(color)}' for color in range(100, 16777000, int(16777000/len(nodes)))][:-1],
    )
    net.add_edges(edges)

    net.show(filename)
