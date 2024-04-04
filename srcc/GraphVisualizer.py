from typing import List, Any

import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, G, pos, central_circle, middle_circle, outer_circle, output_file):
        """Визуализация графа с кольцами."""
        fig, ax = plt.subplots()

        nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=100)
        nx.draw_networkx_edges(G, pos=pos, edge_color='black', width=0.4, arrows=True)

        # for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        #     nx.draw_networkx_nodes(G, pos=pos, nodelist=group, node_size=100, node_color='none', edgecolors='black',
        #                            linewidths=0.5)  Этот код нужен для подчеркивания вершин

        for i, group in enumerate([central_circle, middle_circle, outer_circle]):
            radius = (i + 1) * 5
            circle = plt.Circle((0, 0), radius, color='none', ec='black', linestyle='dashed', linewidth=0.5)
            ax.add_patch(circle)

        labels = {node: node for node in G.nodes}
        nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)

        ax.set_aspect('equal', adjustable='datalim')

        plt.savefig(output_file, dpi=150)  # Сохранение изображения
        plt.close()

#
    # def visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_file):
    #     """Визуализация графа с кольцами."""
    #     fig, ax = plt.subplots()
    #
    #     nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=100)
    #     nx.draw_networkx_edges(G, pos=pos, edge_color='black', width=0.4, arrows=True)
    #
    #     # for i, group in enumerate([central_circle, middle_circle, outer_circle]):
    #     #     nx.draw_networkx_nodes(G, pos=pos, nodelist=group, node_size=100, node_color='none', edgecolors='black',
    #     #                            linewidths=0.5)  Этот код нужен для подчеркивания вершин
    #
    #     for i, group in enumerate([central_circle, middle_circle, outer_circle]):
    #         radius = (i + 1) * 5
    #         circle = plt.Circle((0, 0), radius, color='none', ec='black', linestyle='dashed', linewidth=0.5)
    #         ax.add_patch(circle)
    #
    #     labels = {node: node for node in G.nodes}
    #     nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)
    #
    #     ax.set_aspect('equal', adjustable='datalim')
    #
    #     plt.savefig(output_file, dpi=150)  # Сохранение изображения
    #     plt.close()

