import pandas as pd

INPUT_FILE = "vgsales.csv"        # ← сюда подставь свой файл
OUTPUT_FILE = "data/vgsales_clean.csv"
REPORT_FILE = "data/cleaning_report.txt"

def clean_dataset():
    # Загружаем
    df = pd.read_csv(INPUT_FILE)

    report_lines = []
    report_lines.append("ОТЧЁТ ОБ ОЧИСТКЕ ДАННЫХ\n")
    report_lines.append(f"Исходная форма: {df.shape}\n")
    report_lines.append("Количество пропусков до очистки:\n")
    report_lines.append(str(df.isnull().sum()))
    report_lines.append("\n--------------------------\n")

    # Разделяем типы колонок
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    # Заполнение числовых медианами
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median = df[col].median()
            df[col].fillna(median, inplace=True)
            report_lines.append(f"Числовая колонка '{col}' → заполнена медианой: {median}")

    # Заполнение категориальных модой
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode = df[col].mode()[0]
            df[col].fillna(mode, inplace=True)
            report_lines.append(f"Категориальная колонка '{col}' → заполнена модой: {mode}")

    report_lines.append("\n--------------------------\n")
    report_lines.append(f"Форма после очистки: {df.shape}\n")
    report_lines.append("Количество пропусков после очистки:\n")
    report_lines.append(str(df.isnull().sum()))

    # Сохраняем очищенный датасет
    df.to_csv(OUTPUT_FILE, index=False)

    # Записываем отчёт
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("Очистка завершена ✔")
    print(f"Очищенный файл: {OUTPUT_FILE}")
    print(f"Отчёт: {REPORT_FILE}")

if __name__ == "__main__":
    clean_dataset()