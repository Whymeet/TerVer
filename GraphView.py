import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def read_excel_data(file_path):
    """Считывание данных из файла Excel."""
    return pd.read_excel(file_path, sheet_name='Лист1', index_col=0)


def calculate_statistics(df):
    """Вычисление статистик."""
    V_Plus = df.sum(axis=1).tolist()
    B_Plus = df.sum(axis=0).tolist()
    emotional_expansiveness = [(v / (df.shape[0] - 1)) for v in V_Plus]
    sociometric_status = [(b / (df.shape[0] - 1)) for b in B_Plus]

    return V_Plus, B_Plus, emotional_expansiveness, sociometric_status


def create_directed_graph(df):
    """Создание ориентированного графа."""
    G = nx.DiGraph()

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i, j] == 1:
                G.add_edge(i + 1, j + 1)

    return G


def visualize_graph(G, pos):
    """Визуализация графа."""
    nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
    plt.show()


def main():
    # Путь к файлу Excel
    file_path = r'D:\Unik\TerVer\data\Книга1_тест.xlsx'

    # Считываем данные
    df = read_excel_data(file_path)
    print(df)

    # Вычисляем статистики
    V_Plus, B_Plus, emotional_expansiveness, sociometric_status = calculate_statistics(df)
    print(V_Plus, B_Plus, emotional_expansiveness, sociometric_status, sep='\n')

    # Создаем ориентированный граф
    G = create_directed_graph(df)

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

    # Визуализируем граф
    visualize_graph(G, pos)


if __name__ == "__main__":
    main()
