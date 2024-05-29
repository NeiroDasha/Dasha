import pandas as pd
import zipfile
import os
import matplotlib.pyplot as plt

# Переход на бэкенд 'Agg' для Matplotlib
import matplotlib
matplotlib.use('Agg')

# Путь к скачанному и распакованному архиву Верховного суда
archive_path_supreme_court = r'C:\Users\dasha\OneDrive\Рабочий стол\archive.zip'  # Укажите корректный путь
csv_filename_supreme_court = 'database.csv'

# Директория для распаковки
extract_dir_supreme_court = r'C:\Users\dasha\OneDrive\Рабочий стол'

# Распаковка архива Верховного суда
with zipfile.ZipFile(archive_path_supreme_court, 'r') as zip_ref:
    zip_ref.extractall(extract_dir_supreme_court)  # Укажите директорию для распаковки

# Проверка наличия файла Верховного суда
csv_path_supreme_court = os.path.join(extract_dir_supreme_court, csv_filename_supreme_court)
if os.path.exists(csv_path_supreme_court):
    print(f"Файл {csv_filename_supreme_court} успешно распакован.")
else:
    print(f"Файл {csv_filename_supreme_court} не найден в архиве.")

# Чтение CSV-файла Верховного суда в DataFrame
df_supreme_court = pd.read_csv(csv_path_supreme_court)

# Проверка столбцов
print("\nИмена столбцов в CSV-файле:")
print(df_supreme_court.columns.tolist())

# Анализ данных в столбце, содержащем даты
if 'date_decision' in df_supreme_court.columns:
    df_supreme_court['year'] = pd.to_datetime(df_supreme_court['date_decision'], errors='coerce').dt.year

# Маппинг значений столбца case_disposition для улучшения читаемости
case_disposition_mapping = {
    1: 'Отменено',
    2: 'Утверждено',
    3: 'Аннулировано',
    4: 'Возвращено',
    5: 'Отклонено',
    6: 'Отказано',
    7: 'Сертификат выдан',
    # Добавьте другие соответствия здесь
}

# Применение маппинга
df_supreme_court['case_disposition'] = df_supreme_court['case_disposition'].map(case_disposition_mapping)

# Пропуск значений, которые не удалось маппировать
df_supreme_court = df_supreme_court.dropna(subset=['case_disposition'])

# Агрегатные функции для решений суда
df_agg_disposition = df_supreme_court.groupby(['year', 'case_disposition']).size().reset_index(name='case_count')

# Визуализация данных по решениям суда (case_disposition) для всех лет
plt.figure(figsize=(12, 8))
for disposition in df_agg_disposition['case_disposition'].unique():
    df_plot = df_agg_disposition[df_agg_disposition['case_disposition'] == disposition]
    plt.plot(df_plot['year'], df_plot['case_count'], label=disposition)
plt.xlabel('Год')
plt.ylabel('Количество дел')
plt.title('Количество дел Верховного суда по типу решения')
plt.legend()
plt.savefig('supreme_court_cases_by_disposition.png')
plt.close()

print("График анализа решений суда сохранен в файл 'supreme_court_cases_by_disposition.png'.")
