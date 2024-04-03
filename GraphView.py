import os
import shutil
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from openpyxl.drawing.image import Image

# Получение текущей директории скрипта
current_directory = os.path.dirname(os.path.abspath(__file__))

def get_data_path(path, *args):
    """Функция для получения относительного пути в папку data."""
    return os.path.join(current_directory, path, *args)

def calculate_statistics(df):
    """Вычисление статистик."""
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

    S_group = round(V_vz_plus / V_n_plus, 2) * 100
    Э_group = round(V_n_plus / N, 2)
    BB_group = round((100 * V_vz_plus) / (0.5 * N * (N - 1)), 2)

    C_plus = []
    Э_plus = []
    KUO = []
    column_length = df.shape[0]
    for i in range(1, df.shape[0] + 1):
        sum_column = df[i].sum()
        sum_row = df.loc[i].sum()
        C_plus.append(round(sum_column / (column_length - 1), 3))
        Э_plus.append(round(sum_row / (column_length - 1), 3))

        if sum_row == 0:
            KUO.append('inf')
        else:
            KUO.append(round(sum_column / sum_row, 3))

    return S_group, Э_group, BB_group, C_plus, Э_plus, KUO

def create_directed_graph(df):
    """Создание ориентированного графа."""
    G = nx.DiGraph()

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df.iloc[i, j] == 1:
                G.add_edge(i + 1, j + 1)

    return G

def create_mutual_choice_graph(df):
    """Создание графа взаимных выборов."""
    G_mutual = nx.Graph()

    for i in range(df.shape[0]):
        for j in range(i + 1, df.shape[1]):
            if df.iloc[i, j] == 1 and df.iloc[j, i] == 1:
                G_mutual.add_edge(i + 1, j + 1)

    return G_mutual

def visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_file):
    """Визуализация графа с кольцами."""
    fig, ax = plt.subplots()

    nx.draw_networkx_nodes(G, pos=pos, node_color='skyblue', node_size=100)
    nx.draw_networkx_edges(G, pos=pos, edge_color='black', width=1, arrows=True)

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

def create_new_sheets_with_statistics(input_file_path, output_file_path, img_path):
    """
    Создает новый файл Excel, добавляет в него статистику и изображение, сохраняет результат.

    Параметры:
    - input_file_path (str): Путь к исходному файлу Excel.
    - output_file_path (str): Путь к создаваемому файлу Excel с добавленной статистикой.
    - img_path (str): Путь к изображению для вставки в созданный файл Excel.
    """
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        for sheet_number in range(1, 7):
            # Добавление номера листа к имени файла изображения
            img_path_with_sheet = img_path[:-5] + str(sheet_number) + '.png'

            df = pd.read_excel(input_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)
            S_group, Э_group, BB_group, C_plus, Э_plus, KUO = calculate_statistics(df)

            df.to_excel(writer, sheet_name=f'Лист{sheet_number}')  # Сохраняем исходный лист

            new_sheet_name = f'Статистика{sheet_number}'
            df_statistics = pd.DataFrame({
                'S_group': [S_group],
                'Э_group': [Э_group],
                'BB_group': [BB_group],
            })

            # Identify the appropriate start coordinates
            startcol = max(df.shape[1] - 21, 1)
            startrow = 0

            df_statistics.to_excel(writer, sheet_name=new_sheet_name, startcol=startcol, startrow=startrow)

            df_extended = pd.DataFrame({
                'C_plus': C_plus,
                'Э_plus': Э_plus,
                'КУО': KUO,
            }, index=df.index)

            df_extended.to_excel(writer, sheet_name=new_sheet_name)

            workbook = writer.book
            sheet = workbook[new_sheet_name]
            img = Image(img_path_with_sheet)
            sheet.add_image(img, 'I1')

def main(input_file_path, output_file_path, output_image_file):
    """
    Основная функция, выполняющая анализ данных, визуализацию графа и создание нового файла Excel с результатами.

    Параметры:
    - input_file_path (str): Путь к исходному файлу Excel.
    - output_file_path (str): Путь к создаваемому файлу Excel с добавленной статистикой.
    - output_image_file (str): Путь к изображению для вставки в созданный файл Excel.
    """

    shutil.copy(input_file_path, output_file_path)

    for sheet_number in range(1, 7):
        # Добавление номера листа к имени файла изображения
        output_image_file_with_sheet = output_image_file[:-5] + str(sheet_number) + '.png'

        df = pd.read_excel(output_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)

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

        visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_image_file_with_sheet)

        G = create_mutual_choice_graph(df)

        node_degrees = dict(G.degree())  # Изменено на .degree()
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

        visualize_graph_and_save(G, pos, central_circle, middle_circle, outer_circle, output_image_file_with_sheet)

    create_new_sheets_with_statistics(input_file_path, output_file_path, output_image_file)

if __name__ == "__main__":
    data_directory = get_data_path('data')  # Указываем путь к папке 'data'
    output_directory = get_data_path('output')  # Указываем путь к папке 'output'


    # Проверяем, существует ли папка "output"
    if not os.path.exists(output_directory):
        # Если нет, то создаем ее
        os.makedirs(output_directory)

    # Получаем список файлов в папке "data"
    excel_files = [file for file in os.listdir(data_directory) if file.endswith('.xlsx')]

    # Перебираем каждый файл и обрабатываем его
    for excel_file in excel_files:
        input_file_path = os.path.join(data_directory, excel_file)
        output_file_path = os.path.join(output_directory, f'Выходные данные_{excel_file}')
        output_image_file = os.path.join(output_directory, f'Graph_{excel_file.replace(".xlsx", ".png")}')
        print(output_image_file)
        main(input_file_path, output_file_path, output_image_file)
