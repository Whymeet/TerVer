from typing import List, Any

import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from insrc.I_Graph import I_Graph


class Graph(I_Graph):
    def __init__(self, dataframe):
        self.df = dataframe
        self.G = nx.DiGraph()
        self._create_directed_graph()

    def get_graph(self):
        return self.G

    def _create_directed_graph(self):
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                if self.df.iloc[i, j] == 1:
                    self.G.add_edge(i + 1, j + 1)

    def _add_edge(self, source, target):
        self.G.add_edge(source, target)

    def _remove_edge(self, source, target):
        self.G.remove_edge(source, target)

    def sort_graph(self):
        if self.G is None:
            raise ValueError("Graph is not created.")
        node_degrees = dict(self.G.in_degree())
        sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)
        return sorted_nodes
