from srcc.Graph import Graph
from srcc.GraphVisualizer import GraphVisualizer
import pandas as pd
# Пример использования
input_file_path = "/home/mufus/PycharmProjects/TerVer/data/Data_Socio_2024_ctud_3.xlsx"

sheet_number = 1

df = pd.read_excel(input_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)
graph = Graph(df)
sorted_nodes = graph.sort_graph()
visualizer = GraphVisualizer(graph)
visualizer.visualize()
visualizer.save_figure('/home/mufus/PycharmProjects/TerVer/output/out.png')

