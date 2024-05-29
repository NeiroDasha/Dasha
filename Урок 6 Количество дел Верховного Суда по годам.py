import pandas as pd
import zipfile
import os
import matplotlib.pyplot as plt

# Переход на бэкенд 'Agg' для Matplotlib
import matplotlib
matplotlib.use('Agg')

# Путь к скачанному и распакованному архиву
archive_path = r'C:\Users\dasha\OneDrive\Рабочий стол\archive.zip'  # Укажите корректный путь
csv_filename = 'database.csv'

# Директория для распаковки
extract_dir = r'C:\Users\dasha\OneDrive\Рабочий стол'

# Распаковка архива
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)  # Укажите директорию для распаковки

# Проверка наличия файла
csv_path = os.path.join(extract_dir, csv_filename)
if os.path.exists(csv_path):
    print(f"Файл {csv_filename} успешно распакован.")
else:
    print(f"Файл {csv_filename} не найден в архиве.")

# Чтение CSV-файла в DataFrame
df = pd.read_csv(csv_path)

# Вывод первых нескольких строк DataFrame
print("Первые 5 строк из CSV-файла:")
print(df.head())

# Проверка столбцов
print("\nИмена столбцов в CSV-файле:")
print(df.columns.tolist())

# Анализ данных в столбце, содержащем даты
if 'date_decision' in df.columns:
    df['year'] = pd.to_datetime(df['date_decision'], errors='coerce').dt.year

    # Фильтрация данных за определенный год (например, 2016)
    df_filtered = df[df['year'] == 2016]
    print(f"\nПервые 5 строк из дел за 2016 год:")
    print(df_filtered.head())

    # Агрегатные функции (например, количество дел по годам)
    df_agg = df.groupby('year').size().reset_index(name='case_count')
    print("\nКоличество дел по годам:")
    print(df_agg)

    # Визуализация данных
    plt.figure(figsize=(10, 6))
    plt.bar(df_agg['year'], df_agg['case_count'])
    plt.xlabel('Год')
    plt.ylabel('Количество дел')
    plt.title('Количество дел Верховного Суда по годам')
    plt.xticks(rotation=90)
    plt.savefig('Количество_дел_Верховного_Суда_по_годам.png')
    plt.close()
else:
    print("Столбец 'date_decision' не найден в CSV-файле.")
