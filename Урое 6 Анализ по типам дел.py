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

    # Пример маппинга для issue и issue_area
    issue_description_mapping = {
        10110: 'Уголовное судопроизводство',
        20130: 'Гражданские права',
        30170: 'Первая поправка',
        80180: 'Экономическая деятельность',
        # Добавьте другие соответствия здесь
    }

    issue_area_description_mapping = {
        1: 'Уголовное судопроизводство',
        2: 'Гражданские права',
        3: 'Первая поправка',
        4: 'Должная правовая процедура',
        5: 'Конфиденциальность',
        6: 'Адвокаты',
        7: 'Профсоюзы',
        8: 'Экономическая деятельность',
        9: 'Судебная власть',
        10: 'Федерализм',
        11: 'Межгосударственные отношения',
        12: 'Федеральное налогообложение',
        13: 'Разное',
        14: 'Частные действия',
        # Добавьте другие соответствия здесь
    }

    # Применение маппинга
    df['issue'] = df['issue'].map(issue_description_mapping)
    df['issue_area'] = df['issue_area'].map(issue_area_description_mapping)

    # Пропуск значений, которые не удалось маппировать
    df = df.dropna(subset=['issue', 'issue_area'])

    # Уникальные значения в столбцах 'issue' и 'issue_area'
    unique_issues = df['issue'].unique()
    unique_issue_areas = df['issue_area'].unique()
    print("\nУникальные значения в столбце 'issue':")
    print(unique_issues)
    print("\nУникальные значения в столбце 'issue_area':")
    print(unique_issue_areas)

    # Агрегатные функции (например, количество дел по годам и типам дел)
    df_agg_issue = df.groupby(['year', 'issue']).size().reset_index(name='case_count')
    df_agg_issue_area = df.groupby(['year', 'issue_area']).size().reset_index(name='case_count')

    print("\nКоличество дел по годам и типам (issue):")
    print(df_agg_issue)
    print("\nКоличество дел по годам и типам (issue_area):")
    print(df_agg_issue_area)

    # Визуализация данных по типам дел (issue)
    plt.figure(figsize=(12, 8))
    for issue in unique_issues:
        df_plot = df_agg_issue[df_agg_issue['issue'] == issue]
        plt.plot(df_plot['year'], df_plot['case_count'], label=issue)
    plt.xlabel('Год')
    plt.ylabel('Количество дел')
    plt.title('Количество дел Верховного Суда по типам дел')
    plt.legend()
    plt.savefig('Количество_дел_Верховного_Суда_по_типам_дел.png')
    plt.close()  # Закрытие текущей фигуры для предотвращения наложения графиков

    # Визуализация данных по типам дел (issue_area)
    plt.figure(figsize=(12, 8))
    for issue_area in unique_issue_areas:
        df_plot = df_agg_issue_area[df_agg_issue_area['issue_area'] == issue_area]
        plt.plot(df_plot['year'], df_plot['case_count'], label=issue_area)
    plt.xlabel('Год')
    plt.ylabel('Количество дел')
    plt.title('Количество дел Верховного Суда по областям права')
    plt.legend()
    plt.savefig('Количество_дел_Верховного_Суда_по_областям_права.png')
    plt.close()  # Закрытие текущей фигуры для предотвращения наложения графиков

    print("Графики сохранены в файлы 'Количество_дел_Верховного_Суда_по_типам_дел.png' и 'Количество_дел_Верховного_Суда_по_областям_права.png'.")
else:
    print("Столбец 'date_decision' не найден в CSV-файле.")
