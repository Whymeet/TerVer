import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import shutil
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Загрузка данных из файла Excel
def pers_data(df):
    """
    Выводит статистику по каждому участнику.

    Параметры:
    - df (pd.DataFrame): Исходные данные.
    """
    column_length = df.shape[0]
    for i in range(1, df.shape[0] + 1):
        sum_column = df[i].sum()
        sum_row = df.loc[i].sum()
        print(f' {i}-ый участник\nC+ = {round(sum_column / (column_length - 1), 3)}')
        print(f'Э+ = {round(sum_row / (column_length - 1), 3)}')
        if sum_row == 0:
            print(f'КУО = inf')
        else:
            print(f'КУО = {sum_column / sum_row}')


def S_group(df):
    """
    Выводит статистику по группе.

    Параметры:
    - df (pd.DataFrame): Исходные данные.
    """
    V_n_plus = 0
    N = df.shape[0]
    for i in range(1, df.shape[0] + 1):
        V_n_plus += df.loc[i].sum()
    V_vz_plus = 0
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i, j] == 1 and df.iloc[j, i] == 1:
                V_vz_plus += 1
    V_vz_plus //= 2
    print(f"S_group = {round(V_vz_plus / V_n_plus, 2) * 100}")
    print(f"Э_group = {round(V_n_plus / N, 2)}")
    print(f"BB_group = {round((100 * V_vz_plus) / (0.5 * N * (N - 1)), 2)}")


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


def visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_file):
    """Визуализация графа с кольцами."""
    fig, ax = plt.subplots()

    # Рисуем граф с тонкими рёбрами
    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=100)  # Уменьшаем размер вершин
    nx.draw_networkx_edges(G, pos=pos, edge_color='black', width=0.1, arrows=True)  # Задаем тонкие рёбра

    # Рисуем вершины с использованием кругов
    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        nx.draw_networkx_nodes(G, pos=pos, nodelist=group, node_size=100, node_color='none', edgecolors='black',
                               linewidths=0.5)  # Уменьшаем размер вершин и задаем тонкие обводки

    # Рисуем кольца
    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        radius = (i + 1) * 5
        circle = plt.Circle((0, 0), radius, color='none', ec='black', linestyle='dashed',
                            linewidth=0.5)  # Задаем тонкие линии для кругов
        ax.add_patch(circle)

    # Добавляем метки вершин
    labels = {node: node for node in G.nodes}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)

    ax.set_aspect('equal', adjustable='datalim')

    plt.savefig(output_file, dpi=100)
    plt.close()


def create_new_sheet_with_statistics(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path, sheet_name='Лист1', index_col=0)
    V_Plus, B_Plus, emotional_expansiveness, sociometric_status = calculate_statistics(df)


    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Лист1')

        new_sheet_name = 'Статистика'
        df_statistics = pd.DataFrame({
            'V_Plus': V_Plus,
            'B_Plus': B_Plus,
            'Emotional_Expansiveness': emotional_expansiveness,
            'Sociometric_Status': sociometric_status
        }, index=df.index)

        df_statistics.to_excel(writer, sheet_name=new_sheet_name)

        workbook = writer.book
        sheet = workbook[new_sheet_name]
        img_path = r'D:\Unik\TerVer\data\image.png'
        img = Image(img_path)
        sheet.add_image(img, 'I1')

def main():
    # Пути к файлам Excel
    input_file_path = r'D:\Unik\TerVer\data\Книга1_тест.xlsx'
    output_file_path = r'D:\Unik\TerVer\data\Книга1_тест_со_статистикой.xlsx'

    # Создаем копию файла Excel
    shutil.copy(input_file_path, output_file_path)

    # Считываем данные из копии файла
    df = pd.read_excel(output_file_path, sheet_name='Лист1', index_col=0)
    print(df)

    # Вычисляем статистики
    V_Plus, B_Plus, emotional_expansiveness, sociometric_status = calculate_statistics(df)
    pers_data(df)
    S_group(df)

    # Создаем ориентированный граф
    G = create_directed_graph(df)

    # Получаем словарь, содержащий количество вхождений для каждой вершины
    node_degrees = dict(G.in_degree())

    # Сортируем вершины по количеству вхождений в убывающем порядке
    sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)

    # Разбиваем вершины на три группы в соответствии с их количеством вхождений
    num_groups = 3
    nodes_per_group = len(sorted_nodes) // num_groups
    remainder = len(sorted_nodes) % num_groups

    central_circle = sorted_nodes[:nodes_per_group + remainder]
    middle_circle = sorted_nodes[nodes_per_group + remainder:2 * nodes_per_group + remainder]
    outer_circle = sorted_nodes[2 * nodes_per_group + remainder:]

    # Размещаем вершины на оболочках, формируя круги для каждой группы
    pos = {}
    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        theta = np.linspace(0, 2 * np.pi, len(group), endpoint=False)
        radius = (i + 1) * 5  # Увеличиваем радиус для каждой группы в 5 раз
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        for node, (xx, yy) in zip(group, zip(x, y)):
            pos[node] = (xx, yy)

    # Визуализируем граф с кольцами
    output_image_file = r"D:\Unik\TerVer\data\image.png"
    visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_image_file)

    # Добавляем статистику в созданный файл Excel
    create_new_sheet_with_statistics(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
