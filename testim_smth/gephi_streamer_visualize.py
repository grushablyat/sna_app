from gephistreamer import graph, streamer
import random as rnd


# stream = streamer.Streamer(streamer.GephiWS(
#     hostname='localhost',
#     port=8080,
#     workspace='workspace1'
# ))

szfak = 25
cdfak = 3000


def create_gephi_test():
    stream = streamer.Streamer(streamer.GephiWS(hostname='localhost', port=8080, workspace='workspace1'))

    node_a = graph.Node('A', custom_property=1)
    node_b = graph.Node('B')
    node_b.property['custom_property'] = 2

    nodes = [node_a, node_b]
    stream.add_node(*nodes)

    edge_ab = graph.Edge(node_a, node_b, custom_property='hola')
    stream.add_edge(edge_ab)


def create_gephi_graph(nodes: list, edges: list):
    stream = streamer.Streamer(streamer.GephiWS(hostname='localhost', port=8080, workspace='workspace1'))

    for _ in range(3):
        stream.add_node(*[graph.Node(
            node,
            size=szfak,
            x=cdfak * rnd.random(),
            y=cdfak * rnd.random(),
            color="#ff8080",
            type="p",
        ) for node in nodes])
        stream.add_edge(*[graph.Edge(edge[0], edge[1], eid=f'e{edge[0]}_{edge[1]}', directed=False) for edge in edges])
