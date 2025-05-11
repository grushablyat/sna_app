import networkx as nx
from networkx.algorithms.community import louvain_communities, modularity
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


class SocialNetworkAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()
        self.betweenness = {}
        self.eigenvector = {}
        self.pagerank = {}
        self.communities = []
        self.partition = {}
        self.modularity_score = 0.0
        self.results = None
        self.nodes = None
        self.edges = None

    def load_from_edges(self, friends=None, relations=None):
        if relations is None or not relations:
            print("Ошибка: ребра не предоставлены или пусты")
            return False

        self.graph.clear()

        self.nodes = pd.DataFrame.from_records([friend.to_dict() for friend in friends], columns=['N', 'ID', 'Name'])
        self.edges = pd.DataFrame(list(relations), columns=['Source', 'Target'])

        # Проверка наличия требуемых столбцов
        required_edge_cols = ['Source', 'Target']
        required_node_cols = ['N', 'ID', 'Name']
        if not all(col in self.edges.columns for col in required_edge_cols):
            print(f'Ошибка: отсутствуют атрибуты ребер {required_edge_cols}')
            return {'data': [], 'layout': go.Layout(title='Ошибка: отсутствуют атрибуты ребер')}
        if not all(col in self.nodes.columns for col in required_node_cols):
            print(f'Ошибка: отсутствуют атрибуты узлов {required_node_cols}')
            return {'data': [], 'layout': go.Layout(title='Ошибка: отсутствуют атрибуты узлов')}

        # Создание граф
        self.graph = nx.from_pandas_edgelist(self.edges, 'Source', 'Target', create_using=nx.Graph())

        print(f'Граф создан: узлов={self.graph.number_of_nodes()}, ребер={self.graph.number_of_edges()}')
        return True

    def calculate_centralities(self):
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        # Посредническая центральность
        self.betweenness = nx.betweenness_centrality(self.graph, normalized=True)

        # Собственная центральность
        try:
            self.eigenvector = nx.eigenvector_centrality(self.graph, max_iter=1000, tol=1e-06)
        except nx.PowerIterationFailedConvergence:
            self.eigenvector = {node: 0 for node in self.graph.nodes()}

        # PageRank
        self.pagerank = nx.pagerank(self.graph, alpha=0.85)

    def detect_communities(self, resolution=1.0, seed=42):
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

    def save_results(self, metrics_filename='network_metrics.csv'):
        if not self.graph.nodes:
            print("Ошибка: граф пуст")
            return

        node_attributes = self.nodes.set_index('N')[['Name']].to_dict()
        users_names = node_attributes.get('Name', {})

        results = {
            'ID': list(self.graph.nodes()),
            'Имя': [users_names.get(node, 'Unknown') for node in self.graph.nodes()],
        }

        if self.betweenness:
            results['Посредническая центральность'] = [self.betweenness.get(node, 0) for node in self.graph.nodes()]
        if self.eigenvector:
            results['Степень влиятельности'] = [self.eigenvector.get(node, 0) for node in self.graph.nodes()]
        if self.pagerank:
            results['PageRank'] = [self.pagerank.get(node, 0) for node in self.graph.nodes()]
        if self.communities and self.partition:
            results['Сообщества'] = [self.partition.get(node, -1) for node in self.graph.nodes()]

        if not self.betweenness \
            and not self.eigenvector \
            and not self.pagerank \
            and not self.communities \
            and not self.partition:
            print('Ошибка: метрики не вычислены')
            return

        self.results = pd.DataFrame(results)
        self.results = self.results.sort_values(by='ID', ascending=True)
        self.results.to_csv(metrics_filename, index=False)

    def create_interactive_graph(self, target_user_id, layout_algorithm='spring'):

        # Создание множества уникальных пользователей
        users = set(self.edges['Source']).union(set(self.edges['Target']))
        print(f'Число уникальных счетов: {len(users)}')

        # Определение оболочек для раскладки shell
        shells = [[target_user_id], [ele for ele in users if ele != target_user_id]]

        # Установка атрибутов узлов
        node_attributes = self.nodes.set_index('N')[['ID', 'Name']].to_dict()
        users_names = node_attributes.get('Name', {})
        users_ids = node_attributes.get('ID', {})

        for node in self.graph.nodes():
            self.graph.nodes[node]['Name'] = users_names.get(node, 'Неизвестно1')
            self.graph.nodes[node]['ID'] = users_ids.get(node, 'Неизвестно1')

        # Определение цветов узлов
        if self.partition:
            max_community = max(self.partition.values()) if self.partition else -1
            cmap = plt.get_cmap('tab20', max_community + 1) if max_community >= 0 else None
            colors = [self.partition.get(node, -1) for node in self.graph.nodes()]
        else:
            colors = '#ff9f0f'
            cmap = None

        # Выбор раскладки
        layout_functions = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'kamada_kawai': nx.kamada_kawai_layout,
            'spectral': nx.spectral_layout,
            'random': nx.random_layout,
            'shell': lambda G: nx.shell_layout(G, shells)
        }

        if layout_algorithm not in layout_functions:
            layout_algorithm = 'spring'

        try:
            pos = layout_functions[layout_algorithm](self.graph)
            # Проверка наличия координат у всех узлов
            missing_nodes = set(self.graph.nodes()) - set(pos.keys())
            if missing_nodes:
                print(f'Предупреждение: узлы без координат {missing_nodes}. Присваиваются координаты [0, 0].')
                for node in missing_nodes:
                    pos[node] = [0, 0]
        except Exception as e:
            print(f'Ошибка вычисления раскладки: {e}. Используется раскладка spring.')
            pos = nx.spring_layout(self.graph)

        # Нормализация координат для предотвращения наложения
        x_coords = [pos[node][0] for node in self.graph.nodes()]
        y_coords = [pos[node][1] for node in self.graph.nodes()]
        x_min, x_max = min(x_coords, default=0), max(x_coords, default=1)
        y_min, y_max = min(y_coords, default=0), max(y_coords, default=1)
        if x_max == x_min:
            x_max = x_min + 1
        if y_max == y_min:
            y_max = y_min + 1

        for node in self.graph.nodes():
            x, y = pos[node]
            # Нормализация в диапазон [-1, 1]
            pos[node] = [
                2 * (x - x_min) / (x_max - x_min) - 1 if x_max != x_min else 0,
                2 * (y - y_min) / (y_max - y_min) - 1 if y_max != y_min else 0
            ]
            self.graph.nodes[node]['pos'] = list(pos[node])

        # Проверка наличия атрибута pos
        nodes_without_pos = [node for node in self.graph.nodes() if 'pos' not in self.graph.nodes[node]]
        if nodes_without_pos:
            print(f'Ошибка: узлы без атрибута \'pos\': {nodes_without_pos}. Присваиваются [0, 0].')
            for node in nodes_without_pos:
                self.graph.nodes[node]['pos'] = [0, 0]

        # Обработка случая отсутствия связей
        if not shells[1] or self.graph.number_of_edges() == 0:
            print('Граф не содержит связей.')
            traceRecode = [
                go.Scatter(
                    x=[0], y=[0], text=[str(target_user_id)], textposition='bottom center',
                    mode='markers+text', marker={'size': 50, 'color': 'LightSkyBlue'}
                ),
                go.Scatter(
                    x=[0], y=[0], mode='markers', marker={'size': 50, 'color': 'LightSkyBlue'}, opacity=0
                )
            ]
            return {
                'data': traceRecode,
                'layout': go.Layout(
                    title='Интерактивная визуализация транзакций (Нет связей)',
                    showlegend=False,
                    margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                    xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                    yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                    height=600
                )
            }

        traceRecode = []

        for i, edge in enumerate(self.graph.edges()):
            x0, y0 = self.graph.nodes[edge[0]]['pos']
            x1, y1 = self.graph.nodes[edge[1]]['pos']
            trace = go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode='lines', line={'width': 0.3},
                marker=dict(color='rgb(80, 80, 80)'),
                line_shape='spline', opacity=1
            )
            traceRecode.append(trace)

        node_trace = go.Scatter(
            x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition='bottom center',
            hoverinfo="text", marker={'size': [], 'color': []}
        )
        for node in self.graph.nodes():
            x, y = self.graph.nodes[node]['pos']
            user_id = self.graph.nodes[node].get('ID', 'Неизвестно2')
            customer_name = self.graph.nodes[node].get('Name', 'Неизвестно2')

            if self.betweenness:
                node_size = self.betweenness.get(node, 0) * 35 + 15
            else:
                node_size = 15

            community_id = self.partition.get(node, -1)
            if community_id >= 0 and cmap:
                rgb = tuple(int(c * 255) for c in cmap(community_id)[:3])
                node_color = f'rgb({rgb[0]},{rgb[1]},{rgb[2]})'
            else:
                node_color = '#ff9f0f'
            hovertext = (f'ID: {user_id}<br>'
                         f'Имя: {customer_name}<br>'
                         f'Сообщество: {community_id if community_id >= 0 else "Нет"}<br>')
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['hovertext'] += (hovertext,)
            node_trace['text'] += (node,)
            node_trace['marker']['size'] += (node_size,)
            node_trace['marker']['color'] += (node_color,)
        traceRecode.append(node_trace)

        middle_hover_trace = go.Scatter(
            x=[], y=[], hovertext=[], mode='markers', hoverinfo='text',
            marker={'size': 20, 'color': 'LightSkyBlue'}, opacity=0
        )
        for edge in self.graph.edges():
            x0, y0 = self.graph.nodes[edge[0]]['pos']
            x1, y1 = self.graph.nodes[edge[1]]['pos']
            hovertext = f'От: {edge[0]}<br>К: {edge[1]}'
            middle_hover_trace['x'] += ((x0 + x1) / 2,)
            middle_hover_trace['y'] += ((y0 + y1) / 2,)
            middle_hover_trace['hovertext'] += (hovertext,)
        traceRecode.append(middle_hover_trace)

        if not traceRecode:
            print('Ошибка: трассы не созданы.')
            return {'data': [], 'layout': go.Layout(title='Ошибка: не удалось создать визуализацию')}

        figure = {
            'data': traceRecode,
            'layout': go.Layout(
                title=f'Друзья пользователя {target_user_id} (Модулярность: {self.modularity_score:.4f})',
                showlegend=False, hovermode='closest',
                margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                height=600, clickmode='event+select'
            )
        }
        return figure


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