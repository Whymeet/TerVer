import os
import shutil
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


class FileManager:
    @staticmethod
    def copy_file(source, destination):
        shutil.copy(source, destination)

    @staticmethod
    def get_full_path(*path_components):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), *path_components)
print("12asd")

class DataProcessor:
    @staticmethod
    def load_dataframe(path, sheet_name):
        return pd.read_excel(path, sheet_name=sheet_name, index_col=0)

    @staticmethod
    def save_dataframe_to_excel(df, writer, sheet_name):
        df.to_excel(writer, sheet_name=sheet_name)


class DataAnalyzer:
    @staticmethod
    def calculate_statistics(df):
        v_n_plus = df.sum().sum()
        n = df.shape[0]
        # Упрощенный подход к расчету v_vz_plus, избегая проблемы с индексами
        v_vz_plus = sum(df.values.flatten()) - sum(df.max(axis=1))
        return {
            "S_group": f"{round(v_vz_plus / v_n_plus * 100, 3)}%",
            "Э_group": f"{round(v_n_plus / n, 3)}%",
            "BB_group": f"{round((100 * v_vz_plus) / (0.5 * n * (n - 1)), 3)}%",
            "C_plus": [round(df.iloc[:, i].sum() / (n - 1), 3) for i in range(n)],
            "Э_plus": [round(df.iloc[i].sum() / (n - 1), 3) for i in range(n)],
            "KUO": ['inf' if df.iloc[i].sum() == 0 else round(df.iloc[:, i].sum() / df.iloc[i].sum(), 3) for i in range(n)]
        }


class GraphCreator:
    @staticmethod
    def create_directed_graph(df, mutual=False):
        G = nx.DiGraph()
        for i, row in df.iterrows():
            for j, val in enumerate(row):
                if val == 1 and (not mutual or (mutual and df.iloc[j, i] == 1)):
                    G.add_edge(i+1, j+1)  # Учитываем, что индексы начинаются с 1
        return G


class GraphVisualizer:
    @staticmethod
    def visualize_graph_and_save(G, output_file, layout='circular'):
        plt.figure(figsize=(8, 6))
        if layout == 'circular':
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='k')
        plt.savefig(output_file)
        plt.close()

class ExcelManager:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def process_workbook(self):
        FileManager.copy_file(self.input_path, self.output_path)
        writer = pd.ExcelWriter(self.output_path, engine='openpyxl')
        for sheet_name in pd.ExcelFile(self.input_path).sheet_names:
            df = DataProcessor.load_dataframe(self.input_path, sheet_name)
            stats = DataAnalyzer.calculate_statistics(df)
            df_stats = pd.DataFrame(stats)
            DataProcessor.save_dataframe_to_excel(df, writer, sheet_name)
            DataProcessor.save_dataframe_to_excel(df_stats, writer, f"{sheet_name}_stats")
            G = GraphCreator.create_directed_graph(df)
            graph_visualization_path = f"{self.output_path}_{sheet_name}_graph.png"
            GraphVisualizer.visualize_graph_and_save(G, graph_visualization_path)
        # Исправление: использование метода close() для сохранения и закрытия файла Excel.
        writer.close()

def main():
    pm = FileManager()
    data_path = pm.get_full_path('data')
    output_path = pm.get_full_path('output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file in os.listdir(data_path):
        if file.endswith('.xlsx'):
            em = ExcelManager(os.path.join(data_path, file), os.path.join(output_path, f"Processed_{file}"))
            em.process_workbook()

if __name__ == "__main__":
    main()
