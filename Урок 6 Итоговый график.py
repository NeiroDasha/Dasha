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

    # Пример маппинга для issue, issue_area и case_disposition
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
    df['issue'] = df['issue'].map(issue_description_mapping)
    df['issue_area'] = df['issue_area'].map(issue_area_description_mapping)
    df['case_disposition'] = df['case_disposition'].map(case_disposition_mapping)

    # Пропуск значений, которые не удалось маппировать
    df = df.dropna(subset=['issue', 'issue_area', 'case_disposition'])

    # Агрегатные функции (например, количество дел по годам и типам дел)
    df_agg_issue = df.groupby(['year', 'issue']).size().reset_index(name='case_count')
    df_agg_issue_area = df.groupby(['year', 'issue_area']).size().reset_index(name='case_count')
    df_agg_disposition = df.groupby(['year', 'case_disposition']).size().reset_index(name='case_count')

    # Сбор данных по социально-политическим событиям (пример данных)
    events = {
        'Гражданская война в США': 1861,
        'Великая депрессия': 1929,
        'Вторая мировая война': 1939,
        'Движение за гражданские права': 1960,
        'Террористические акты 11 сентября': 2001,
    }

    # Визуализация данных
    fig, axes = plt.subplots(3, 1, figsize=(14, 18), sharex=True)

    # График по типам дел (issue)
    for issue in df_agg_issue['issue'].unique():
        df_plot = df_agg_issue[df_agg_issue['issue'] == issue]
        axes[0].plot(df_plot['year'], df_plot['case_count'], label=issue)
    axes[0].set_ylabel('Количество дел')
    axes[0].set_title('Количество дел Верховного Суда по типам дел')
    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # График по областям права (issue_area)
    for issue_area in df_agg_issue_area['issue_area'].unique():
        df_plot = df_agg_issue_area[df_agg_issue_area['issue_area'] == issue_area]
        axes[1].plot(df_plot['year'], df_plot['case_count'], label=issue_area)
    axes[1].set_ylabel('Количество дел')
    axes[1].set_title('Количество дел Верховного Суда по областям права')
    axes[1].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # График по решениям суда (case_disposition)
    for disposition in df_agg_disposition['case_disposition'].unique():
        df_plot = df_agg_disposition[df_agg_disposition['case_disposition'] == disposition]
        axes[2].plot(df_plot['year'], df_plot['case_count'], label=disposition)
    axes[2].set_xlabel('Год')
    axes[2].set_ylabel('Количество дел')
    axes[2].set_title('Количество дел Верховного Суда по решениям суда')
    axes[2].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Добавление вертикальных линий для социально-политических событий
    for event, year in events.items():
        for ax in axes:
            ax.axvline(x=year, color='gray', linestyle='--', alpha=0.5)
            ax.text(year, ax.get_ylim()[1] * 0.9, event, rotation=90, verticalalignment='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('combined_analysis_with_events.png')
    plt.close()

    print("График анализа с социально-политическими событиями сохранен в файл 'combined_analysis_with_events.png'.")
else:
    print("Столбец 'date_decision' не найден в CSV-файле.")
