import os
import shutil
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from openpyxl.drawing.image import Image

# Определение текущей директории
current_directory = os.path.dirname(os.path.abspath(__file__))

def get_data_path(*args):
    """Функция для получения относительного пути в папку data."""
    return os.path.join(current_directory, 'data', *args)
print(get_data_path("Книга1_тест1.xlszczxcz"))