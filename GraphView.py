import os
import shutil
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image


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

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=100)
    nx.draw_networkx_edges(G, pos=pos, edge_color='black', width=0.1, arrows=True)

    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        nx.draw_networkx_nodes(G, pos=pos, nodelist=group, node_size=100, node_color='none', edgecolors='black',
                               linewidths=0.5)

    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        radius = (i + 1) * 5
        circle = plt.Circle((0, 0), radius, color='none', ec='black', linestyle='dashed', linewidth=0.5)
        ax.add_patch(circle)

    labels = {node: node for node in G.nodes}
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)

    ax.set_aspect('equal', adjustable='datalim')

    plt.savefig(output_file, dpi=100)
    plt.close()


def create_new_sheet_with_statistics(input_file_path, output_file_path, img_path):
    """
    Создает новый файл Excel, добавляет в него статистику и изображение, сохраняет результат.

    Параметры:
    - input_file_path (str): Путь к исходному файлу Excel.
    - output_file_path (str): Путь к создаваемому файлу Excel с добавленной статистикой.
    - img_path (str): Путь к изображению для вставки в созданный файл Excel.
    """
    df = pd.read_excel(input_file_path, sheet_name='Лист1', index_col=0)
    V_Plus, B_Plus, emotional_expansiveness, sociometric_status = calculate_statistics(df)

    if os.path.exists(output_file_path):
        os.remove(output_file_path)

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
        img = Image(img_path)
        sheet.add_image(img, 'I1')


def main():
    """
    Основная функция, выполняющая анализ данных, визуализацию графа и создание нового файла Excel с результатами.

    Параметры:
    - input_file_path (str): Путь к исходному файлу Excel.
    - output_file_path (str): Путь к создаваемому файлу Excel с добавленной статистикой.
    - output_image_file (str): Путь к изображению для вставки в созданный файл Excel.
    """
    input_file_path = r'D:\Unik\TerVer\data\Книга1_тест.xlsx'
    output_file_path = r'D:\Unik\TerVer\data\Книга1_тест_со_статистикой.xlsx'
    output_image_file = r"D:\Unik\TerVer\data\image.png"

    shutil.copy(input_file_path, output_file_path)

    df = pd.read_excel(output_file_path, sheet_name='Лист1', index_col=0)
    print(df)

    pers_data(df)
    S_group(df)

    G = create_directed_graph(df)

    node_degrees = dict(G.in_degree())
    sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)

    num_groups = 3
    nodes_per_group = len(sorted_nodes) // num_groups
    remainder = len(sorted_nodes) % num_groups

    central_circle = sorted_nodes[:nodes_per_group + remainder]
    middle_circle = sorted_nodes[nodes_per_group + remainder:2 * nodes_per_group + remainder]
    outer_circle = sorted_nodes[2 * nodes_per_group + remainder:]

    pos = {}
    for i, group in enumerate([central_circle, middle_circle, outer_circle]):
        theta = np.linspace(0, 2 * np.pi, len(group), endpoint=False)
        radius = (i + 1) * 5
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        for node, (xx, yy) in zip(group, zip(x, y)):
            pos[node] = (xx, yy)

    visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_image_file)

    create_new_sheet_with_statistics(input_file_path, output_file_path, output_image_file)


if __name__ == "__main__":
    main()
