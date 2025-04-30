import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import louvain_communities, modularity
from matplotlib.cm import ScalarMappable
import csv
import json

class SocialNetworkAnalyzer:
    def __init__(self):
        """Инициализация пустого анализатора социальной сети."""
        self.graph = nx.Graph()
        self.betweenness = {}
        self.eigenvector = {}
        self.pagerank = {}
        self.communities = []
        self.partition = {}
        self.modularity_score = 0.0
        self.results = None

    def load_from_edges(self, nodes=None, edges=None):
        """Загрузка графа из списка узлов и ребер."""
        if edges is None or not edges:
            print("Ошибка: ребра не предоставлены или пусты")
            return False
        self.graph.clear()
        if nodes:
            self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        print(f"Граф загружен: {self.graph.number_of_nodes()} узлов, {self.graph.number_of_edges()} ребер")
        return True

    def load_from_file(self, file_path, file_type='edgelist'):
        """Загрузка графа из файла (поддерживаются edgelist или JSON)."""
        self.graph.clear()
        try:
            if file_type == 'edgelist':
                self.graph = nx.read_edgelist(file_path, nodetype=int)
            elif file_type == 'json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.graph = nx.node_link_graph(data)
            else:
                print(f"Ошибка: неподдерживаемый тип файла '{file_type}'")
                return False
            print(f"Граф загружен из файла: {self.graph.number_of_nodes()} узлов, {self.graph.number_of_edges()} ребер")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return False

    def calculate_centralities(self):
        """Расчет метрик центральности (посредническая, собственная, PageRank)."""
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        # Посредническая центральность
        self.betweenness = nx.betweenness_centrality(self.graph, normalized=True)
        print("Междуность рассчитана")

        # Собственная центральность
        try:
            self.eigenvector = nx.eigenvector_centrality(self.graph, max_iter=1000, tol=1e-06)
            print("Собственная центральность рассчитана")
        except nx.PowerIterationFailedConvergence:
            self.eigenvector = {node: 0 for node in self.graph.nodes()}
            print("Собственная центральность не сошлась, используются нули")

        # PageRank
        self.pagerank = nx.pagerank(self.graph, alpha=0.85)
        print("PageRank рассчитан")

    def detect_communities(self, resolution=1.0, seed=42):
        """Обнаружение сообществ с помощью алгоритма Louvain."""
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        self.communities = louvain_communities(self.graph, resolution=resolution, seed=seed)
        self.partition = {}
        for i, comm in enumerate(self.communities):
            for node in comm:
                self.partition[node] = i
        self.modularity_score = modularity(self.graph, self.communities)
        print(f"Сообщества обнаружены: {len(self.communities)} сообществ, модулярность = {self.modularity_score:.3f}")

    def save_results(self, output_file='network_metrics.csv'):
        """Сохранение результатов в CSV."""
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        results = {
            'UserID': list(self.graph.nodes()),
        }

        if self.betweenness:
            results['Betweenness'] = [self.betweenness.get(node, 0) for node in self.graph.nodes()]
        if self.eigenvector:
            results['Eigenvector'] = [self.eigenvector.get(node, 0) for node in self.graph.nodes()]
        if self.pagerank:
            results['PageRank'] = [self.pagerank.get(node, 0) for node in self.graph.nodes()]
        if self.communities and self.partition:
            results['Communities'] = [self.partition.get(node, -1) for node in self.graph.nodes()]

        if not self.betweenness \
            and not self.eigenvector \
            and not self.pagerank \
            and not self.communities \
            and not self.partition:
            print('Ошибка: метрики не вычислены')
            return

        self.results = pd.DataFrame(results)

        self.results = self.results.sort_values(by='Betweenness', ascending=False)
        self.results.to_csv(output_file, index=False)
        print(f"Результаты сохранены в '{output_file}'")
        print("\nТоп-5 узлов по междуности:")
        print(self.results.head())

    def visualize(self, output_file='network_graph.png', labels=True, communities=True):
        """Визуализация графа: цвет по сообществам (если есть), размер по междуности."""
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        fig, ax = plt.subplots(figsize=(10, 8), dpi=500)
        pos = nx.spring_layout(self.graph, seed=42)

        # Размер узлов по междуности
        sizes = [self.betweenness.get(node, 0) * 5000 + 100 for node in self.graph.nodes()]

        # Цвет узлов: по сообществам, если они есть, иначе единый цвет
        if communities and self.partition:
            colors = [self.partition.get(node, -1) for node in self.graph.nodes()]
            max_community = max(self.partition.values())
            cmap = plt.get_cmap('tab20', max_community + 1)
            # Цветовая шкала
            # sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=max_community))
            # fig.colorbar(sm, ax=ax, label='Community')
        else:
            colors = '#ff9f0f'  # Единый цвет, если сообщества не обнаружены
            cmap = None

        # Рисуем узлы и ребра
        nx.draw_networkx_nodes(self.graph, pos, node_color=colors, cmap=cmap, node_size=sizes, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, alpha=0.5, ax=ax)
        if labels:
            nx.draw_networkx_labels(self.graph, pos, font_size=10, ax=ax)

        # plt.title("Social Network Graph: Colored by Community (if detected), Sized by Betweenness")
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"Визуализация сохранена в '{output_file}'")

    def analyze_and_visualize(self, nodes=None, edges=None, input_file=None, file_type='edgelist'):
        """Полный анализ: загрузка, расчет характеристик, сохранение и визуализация."""
        # Загрузка графа
        if input_file:
            self.load_from_file(input_file, file_type)
        else:
            self.load_from_edges(nodes, edges)

        # Расчет характеристик
        self.calculate_centralities()
        self.detect_communities()

        # Сохранение и визуализация
        self.save_results()
        self.visualize()


if __name__ == "__main__":
    # Пример использования
    analyzer = SocialNetworkAnalyzer()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    edges = [
        (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5),
        (5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (8, 9)
    ]
    # Тест с сообществами
    analyzer.analyze_and_visualize(nodes, edges)
    # Тест без сообществ
    analyzer2 = SocialNetworkAnalyzer()
    analyzer2.load_from_edges(nodes, edges)
    analyzer2.calculate_centralities()
    analyzer2.visualize('graph_no_communities.png')