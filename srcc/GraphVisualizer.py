from typing import List, Any

import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph

    def visualize(self, edge_width=2):
        sorted_nodes = self.graph.sort_graph()
        pos = self._calculate_positions(sorted_nodes)
        self._draw(pos)

    def _calculate_positions(self, sorted_nodes):
        pos = {}
        num_groups = 3
        nodes_per_group = len(sorted_nodes) // num_groups
        remainder = len(sorted_nodes) % num_groups

        groups = [sorted_nodes[:nodes_per_group + remainder],
                  sorted_nodes[nodes_per_group + remainder:2 * nodes_per_group + remainder],
                  sorted_nodes[2 * nodes_per_group + remainder:]]

        for i, group in enumerate(groups):
            theta = np.linspace(0, 2 * np.pi, len(group), endpoint=False)
            radius = (i + 1) * 5
            x, y = radius * np.cos(theta), radius * np.sin(theta)
            for node, coord in zip(group, zip(x, y)):
                pos[node] = coord
        return pos

    def _draw(self, pos, edge_width= 0.1):
        plt.figure(figsize=(8, 8))
        ax = plt.gca()
        self._draw_circles(ax)
        nx.draw_networkx_nodes(self.graph.G, pos, node_color='skyblue', node_size=300)
        nx.draw_networkx_edges(self.graph.G, pos, width=edge_width, arrows=True)
        nx.draw_networkx_labels(self.graph.G, pos, font_size=12)
        plt.axis('equal')
       # plt.savefig(output_path, dpi=100)


    def _draw_circles(self, ax):
        base_radius = 5  # Задаем начальный радиус
        num_groups = 3   # Общее количество групп
        for i in range(num_groups):
            radius = base_radius * (i + 1)  # Расчет радиуса для каждого круга
            circle = plt.Circle((0, 0), radius, color='none', ec='black', linestyle='dashed', linewidth=0.5)
            ax.add_patch(circle)

    def save_figure(self, output_file, dpi=100):
        """
        Сохраняет текущую визуализацию графа в файл.

        :param output_file: Путь к файлу, в который будет сохранено изображение.
        :param dpi: Разрешение изображения в точках на дюйм (dots per inch).
        """
        plt.savefig(output_file, dpi=dpi)

