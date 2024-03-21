import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import os
import shutil


class ExcelGraphStatistics:
    def __init__(self, input_file_path, output_file_path, img_path_template):
        # Инициализация класса с путями к файлам и шаблоном пути к изображениям
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.img_path_template = img_path_template

    def process_sheets(self):
        # Удаление выходного файла, если он существует, и копирование входного файла в качестве нового выходного
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
        shutil.copy(self.input_file_path, self.output_file_path)

        try:
            # Создание Excel-файла для записи с использованием pandas ExcelWriter
            with pd.ExcelWriter(self.output_file_path, engine='openpyxl') as writer:
                for sheet_number in range(1, 7):
                    # Чтение листа Excel в DataFrame
                    df = pd.read_excel(self.input_file_path, sheet_name=f'Лист{sheet_number}', index_col=0)
                    # Запись DataFrame обратно в лист Excel
                    df.to_excel(writer, sheet_name=f'Лист{sheet_number}')

                    # Вычисление статистик для DataFrame
                    statistics = self.calculate_statistics(df)
                    # Добавление листа со статистикой и изображением в Excel файл
                    self.add_statistics_sheet(writer, sheet_number, statistics,
                                              self.img_path_template.format(sheet_number))
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def calculate_statistics(self, df):
        # Вычисление статистик для DataFrame
        N = df.shape[0]  # Количество строк в DataFrame
        V_n_plus = df.values.sum()  # Сумма всех значений в DataFrame
        V_vz_plus = (df.values & df.values.T).sum() // 2  # Сумма взаимных связей

        statistics = {
            'S_group': round((V_vz_plus / V_n_plus * 100), 2) if V_n_plus else 0,  # Процент взаимных связей
            'Э_group': round((V_n_plus / N), 2) if N else 0,  # Среднее количество связей на элемент
            'BB_group': round((100 * V_vz_plus) / (0.5 * N * (N - 1)), 2) if N else 0,  # Плотность графа
            'C_plus': [(df.iloc[:, i].sum() / (N - 1)).round(3) for i in range(N)] if N > 1 else [0] * N,
            # Степень центральности по столбцам
            'Э_plus': [(df.iloc[i].sum() / (N - 1)).round(3) for i in range(N)] if N > 1 else [0] * N,
            # Степень центральности по строкам
            'КУО': [(df.iloc[:, i].sum() / df.iloc[i].sum()).round(3) if df.iloc[i].sum() != 0 else 'inf' for i in
                    range(N)]  # Коэффициент устойчивости объекта
        }

        return statistics

    def add_statistics_sheet(self, writer, sheet_number, statistics, img_path):
        # Добавление листа со статистикой и изображением в Excel файл
        new_sheet_name = f'Статистика{sheet_number}'
        df_statistics = pd.DataFrame(statistics)

        startcol = max(df_statistics.shape[1] - 21, 0)
        df_statistics.to_excel(writer, sheet_name=new_sheet_name, startcol=startcol)

        workbook = writer.book
        try:
            sheet = workbook[new_sheet_name]
            img = Image(img_path)
            sheet.add_image(img, 'I1')
        except FileNotFoundError:
            print(f"Файл изображения не найден: {img_path}")
        except Exception as e:
            print(f"Ошибка при добавлении изображения: {e}")
