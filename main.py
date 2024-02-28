# def create_new_sheet_with_statistics(file_path):
#     # Считываем данные
#     df = pd.read_excel(file_path, sheet_name='Лист1', index_col=0)
#
#     # Вычисляем статистики
#     V_Plus, B_Plus, emotional_expansiveness, sociometric_status = calculate_statistics(df)
#
#     # Создаем новый лист с именем 'Статистика'
#     with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
#         # Если файл уже существует, добавляем к нему новый лист
#         new_sheet_name = 'Статистика'
#         df_statistics = pd.DataFrame({
#             'V_Plus': V_Plus,
#             'B_Plus': B_Plus,
#             'Emotional_Expansiveness': emotional_expansiveness,
#             'Sociometric_Status': sociometric_status
#         }, index=df.index)
#
#         df_statistics.to_excel(writer, sheet_name=new_sheet_name)
