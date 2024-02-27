# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Пример считывания данных из файла Excel (замените на свой путь к файлу)
# df = pd.read_excel('Книга1_тест.xlsx', sheet_name='Лист1', index_col=0)
# print(df)
#
# # Создание пустого ориентированного графа
# G = nx.DiGraph()
#
# # Добавление ребер и вершин в граф
# for i in range(df.shape[0]):
#     for j in range(df.shape[1]):
#         if df.iloc[i, j] == 1:
#             G.add_edge(i+1, j+1)
#
# # Получаем словарь, содержащий количество вхождений для каждой вершины
# node_degrees = dict(G.in_degree())
#
# # Сортируем вершины по количеству вхождений в убывающем порядке
# sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)
#
# # Разбиваем вершины на три группы в соответствии с их количеством вхождений
# central_circle = sorted_nodes[:3]
# middle_circle = sorted_nodes[3:6]
# outer_circle = sorted_nodes[6:]
#
# # Размещаем вершины на оболочках
# pos = nx.shell_layout(G, [central_circle, middle_circle, outer_circle])
#
# # Визуализация графа
# nx.draw(G, pos, with_labels=True, font_weight='bold')
#
# # Отображение графа
# plt.show()


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


file_path = r'D:\Unik\TerVerPrjct\dataForprjct\Книга1_тест.xlsx'
# Пример считывания данных из файла Excel (замените на свой путь к файлу)
df = pd.read_excel(file_path, sheet_name='Лист1', index_col=0)
print(df)

B_Plus = []
V_Plus = []
V = 0
emotional_expansiveness = []
KYO = []
sociometric_status = []
for row in range(df.shape[0]):
    V_Plus.append(df.iloc[row, :].sum())
    B_Plus.append(df.iloc[:, row].sum())
    emotional_expansiveness.append(V_Plus[row] / (df.shape[0] - 1))
    sociometric_status.append(B_Plus[row] / (df.shape[0] - 1))
print(V_Plus, B_Plus, emotional_expansiveness, sociometric_status, sep='\n')

# Создание пустого ориентированного графа
G = nx.DiGraph()

# Добавление ребер и вершин в граф
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        if df.iloc[i, j] == 1:
            G.add_edge(i + 1, j + 1)

# Получаем словарь, содержащий количество вхождений для каждой вершины
node_degrees = dict(G.in_degree())

# Сортируем вершины по количеству вхождений в убывающем порядке
sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)

# Разбиваем вершины на три группы в соответствии с их количеством вхождений
central_circle = sorted_nodes[:3]
middle_circle = sorted_nodes[3:6]
outer_circle = sorted_nodes[6:]

# Размещаем вершины на оболочках, формируя круги для каждой группы
pos = {}
num_nodes = len(G.nodes)

for i, group in enumerate([central_circle, middle_circle, outer_circle]):
    theta = np.linspace(0, 2 * np.pi, len(group), endpoint=False)
    radius = i + 1  # Увеличиваем радиус для каждой группы
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    for node, (xx, yy) in zip(group, zip(x, y)):
        pos[node] = (xx, yy)

# Визуализация графа
nx.draw(G, pos=pos, with_labels=True, font_weight='bold')

# Отображение графа
plt.show()
