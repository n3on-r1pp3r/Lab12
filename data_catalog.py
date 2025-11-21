import os
import pandas as pd
from datetime import datetime

# === Укажи здесь нужные файлы ===
FILES_TO_SCAN = [
    "README.md",
    "lab12.ipynb",
    "data_catalog.py",
    "vgsales.csv"     # ← сюда подставь свой датасет
]

OUTPUT_CSV = "data_catalog.csv"


def get_file_metadata(filepath: str) -> dict:
    """Сбор метаданных по одному файлу."""
    stats = os.stat(filepath)
    size = stats.st_size
    modified = datetime.fromtimestamp(stats.st_mtime)

    info = {
        "filename": os.path.basename(filepath),
        "path": filepath,
        "extension": os.path.splitext(filepath)[1],
        "size_bytes": size,
        "modified": modified,
        "rows": None,
        "columns": None,
        "column_names": None,
        "column_types": None,
        "description": "Файл проекта"
    }

    # Читаем CSV, если это CSV
    if info["extension"].lower() == ".csv":
        try:
            df = pd.read_csv(filepath)
            info["rows"] = df.shape[0]
            info["columns"] = df.shape[1]
            info["column_names"] = list(df.columns)
            info["column_types"] = df.dtypes.astype(str).to_dict()
        except Exception as e:
            print(f"Ошибка чтения {filepath}: {e}")

    return info


def generate_catalog():
    """Создание датакаталога по указанным файлам."""
    collected = []

    for filepath in FILES_TO_SCAN:
        if os.path.exists(filepath):
            metadata = get_file_metadata(filepath)
            collected.append(metadata)
        else:
            print(f"⚠ Файл не найден: {filepath}")

    df = pd.DataFrame(collected)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("\nКаталог данных создан ✔")
    print(f"Файл создан: {OUTPUT_CSV}")
    print(f"Файлов обработано: {len(collected)}")


if __name__ == "__main__":
    generate_catalog()