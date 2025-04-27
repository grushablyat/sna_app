import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import louvain_communities, modularity
from matplotlib.cm import ScalarMappable


def analyze_and_vizualize_graph(edges):
    edges = list(edges)
    # 1. Create graph (synthetic data, replace with API data, e.g., VK)
    G = nx.Graph()
    # edges = [
    #     (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5),
    #     (5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (8, 9),
    # ]
    G.add_edges_from(edges)

    # 2. Calculate centrality metrics
    # a) Betweenness Centrality
    betweenness = nx.betweenness_centrality(G, normalized=True)

    # b) Eigenvector Centrality
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
    except nx.PowerIterationFailedConvergence:
        eigenvector = {node: 0 for node in G.nodes()}
        print("Eigenvector centrality failed to converge, using zeros.")

    # c) PageRank
    pagerank = nx.pagerank(G, alpha=0.85)

    # 3. Community detection (Louvain)
    communities = louvain_communities(G, resolution=1.0, seed=42)
    # Create node-to-community mapping
    partition = {}
    for i, comm in enumerate(communities):
        for node in comm:
            partition[node] = i
    # Calculate modularity
    modularity_score = modularity(G, communities)

    # 4. Save results to DataFrame
    results = pd.DataFrame({
        'UserID': list(G.nodes()),
        'Betweenness': [betweenness[node] for node in G.nodes()],
        'Eigenvector': [eigenvector[node] for node in G.nodes()],
        'PageRank': [pagerank[node] for node in G.nodes()],
        'Community': [partition.get(node, -1) for node in G.nodes()]
    })

    # Sort by Betweenness
    results = results.sort_values(by='Betweenness', ascending=False)

    # 5. Export results to CSV
    results.to_csv('network_metrics.csv', index=False)
    print("Results saved to 'network_metrics.csv'")
    print(f"Modularity: {modularity_score:.3f}")
    print("\nTop 5 nodes by Betweenness Centrality:")
    print(results.head())

    # 6. Visualize graph
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Fixed layout for reproducibility

    # Color nodes by community
    colors = [partition.get(node, -1) for node in G.nodes()]
    max_community = max(partition.values()) if partition else 0
    cmap = plt.get_cmap('tab20', max_community + 1)

    # Size nodes by Betweenness
    sizes = [betweenness[node] * 5000 + 100 for node in G.nodes()]

    # Draw nodes and edges
    scatter = nx.draw_networkx_nodes(G, pos, node_color=colors, cmap=cmap, node_size=sizes, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

    # Create colorbar
    sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max_community))
    cbar = fig.colorbar(sm, ax=ax, label='Community')

    plt.title("Social Network Graph: Colored by Community, Sized by Betweenness")
    plt.savefig('network_graph.png')
    plt.close()

    print("Graph visualization saved to 'network_graph.png'")