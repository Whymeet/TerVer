from typing import List, Any

import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, dataframe, use_bin=False):
        self.df = dataframe
        self.G = nx.DiGraph()
        if use_bin:
            self._create_directed_graph_bin()
        else:
            self._create_directed_graph()

    def _create_directed_graph(self):
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                if self.df.iloc[i, j] == 1:
                    self.G.add_edge(i + 1, j + 1)

    def add_edge(self, source, target):
        self.G.add_edge(source, target)

    def remove_edge(self, source, target):
        self.G.remove_edge(source, target)

    def sort_graph(self):
        if self.G is None:
            raise ValueError("Graph is not created.")
        node_degrees = dict(self.G.in_degree())
        sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)
        return sorted_nodes

    def _create_directed_graph_bin(self):
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                if self.df.iloc[i, j] == 1 and self.df.iloc[j, i] == 1:
                    self.G.add_edge(i + 1, j + 1)
