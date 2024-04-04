import os
import shutil
import pandas as pd

from srcc.ExcelStatisticsHandler import ExcelGraphStatistics
from srcc.Graph import Graph
from srcc.GraphVisualizer import GraphVisualizer

 def process():
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
        shutil.copy(self.input_file_path, self.output_file_path)

        with pd.ExcelWriter(self.output_file_path, engine='openpyxl') as writer:
            for sheet_number in range(1, 7):
                df = pd.read_excel(self.input_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)
                graph = Graph(df, True)
                visualizer = GraphVisualizer(graph)

                # Визуализация и сохранение изображения графа
                output_img_path = self.img_path_template.format(sheet_number)
                visualizer.visualize()
                visualizer.save_figure(output_img_path)

                # Сохранение DataFrame в Excel
                df.to_excel(writer, sheet_name=f'Лист{sheet_number}')

                # Добавление статистики и изображений
                excel_stats = ExcelGraphStatistics(self.input_file_path, self.output_file_path, self.img_path_template)
#                 excel_stats.process_sheets()


# # Исправленное объявление функции без self
# def get_data_path(path, *args):
#     return os.path.join(path, *args)
#
# class MainProcessor:
#     def __init__(self, input_file_path, output_file_path, data_directory, output_directory):
#         self.input_file_path = input_file_path
#         self.output_file_path = output_file_path
#         self.data_directory = data_directory
#         self.output_directory = output_directory
#         self.img_path_template = os.path.join(self.output_directory, 'Graph_{}.png')
#
#     def process(self):
#         if os.path.exists(self.output_file_path):
#             os.remove(self.output_file_path)
#         shutil.copy(self.input_file_path, self.output_file_path)
#
#         with pd.ExcelWriter(self.output_file_path, engine='openpyxl') as writer:
#             for sheet_number in range(1, 7):
#                 df = pd.read_excel(self.input_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)
#                 graph = Graph(df, True)
#                 visualizer = GraphVisualizer(graph)
#
#                 # Визуализация и сохранение изображения графа
#                 output_img_path = self.img_path_template.format(sheet_number)
#                 visualizer.visualize()
#                 visualizer.save_figure(output_img_path)
#
#                 # Сохранение DataFrame в Excel
#                 df.to_excel(writer, sheet_name=f'Лист{sheet_number}')
#
#                 # Добавление статистики и изображений
#                 excel_stats = ExcelGraphStatistics(self.input_file_path, self.output_file_path, self.img_path_template)
#                 excel_stats.process_sheets()
#
# if __name__ == "__main__":
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     # Используйте функцию без self
#     data_directory = get_data_path(current_directory, 'data')
#     output_directory = get_data_path(current_directory, 'output')
#
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
#
#     excel_files = [file for file in os.listdir(data_directory) if file.endswith('.xlsx')]
#
#     for excel_file in excel_files:
#         input_file_path = os.path.join(data_directory, excel_file)
#         output_file_path = os.path.join(output_directory, f'Processed_{excel_file}')
#         processor = MainProcessor(input_file_path, output_file_path, data_directory, output_directory)
#         processor.process()
