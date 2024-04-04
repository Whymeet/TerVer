from typing import List, Any

import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from srcc.Graph import Graph


class Graph_Bin(Graph):
    def __init__(self, dataframe):
        super().__init__(dataframe)

    def _create_directed_graph(self):
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                if self.df.iloc[i, j] == 1 and self.df.iloc[j, i] == 1:
                    self.G.add_edge(i + 1, j + 1)


