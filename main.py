from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Создаем новый файл Excel
workbook = Workbook()

# Получаем активный лист
sheet = workbook.active

# Вставляем изображение
img = Image(r'D:\Unik\TerVer\data\image.png')
sheet.add_image(img, 'P10')  # 'A1' - это координаты, где будет вставлено изображение

# Сохраняем файл
workbook.save(r'D:\Unik\TerVer\data\NewTab.xlsx')