import os
import json
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY
import pandas as pd
#from dotenv import load_dotenv

#load_dotenv()
# Настройки подключения и папки для CSV
DATABASE_URL = os.getenv("DATABASE_URL")  # Замените на ваши параметры
CSV_FOLDER = "csv_exports"

# Создаём движок и метаданные
engine = create_engine(DATABASE_URL)
metadata = MetaData()


def safe_serialize(x) -> str:
    """
    Преобразует Python-объект x в JSON-строку.
    Возвращает None, если сериализировать нельзя или x является отсутствующим значением.
    """
    if x is None:
        return None
    try:
        return json.dumps(x, ensure_ascii=False)
    except (TypeError, ValueError):
        return None


def safe_deserialize(x) -> object:
    """
    Преобразует JSON-строку x в Python-объект.
    Возвращает None, если десериализовать нельзя или x является отсутствующим значением.
    """
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    try:
        return json.loads(x)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def export_database_to_csv():
    """
    Экспорт всех таблиц базы данных в CSV-файлы.
    Сортировка по 'id' (если есть) и сериализация JSON-/ARRAY-столбцов.
    """
    metadata.reflect(bind=engine)
    os.makedirs(CSV_FOLDER, exist_ok=True)

    for table_name, table in metadata.tables.items():
        df = pd.read_sql_table(table_name, engine)
        if 'id' in df.columns:
            df = df.sort_values(by='id')

        # Определяем JSON- и ARRAY-столбцы
        json_cols = [col.name for col in table.columns
                     if isinstance(col.type, (JSON, JSONB, ARRAY))]
        for col in json_cols:
            df[col] = df[col].apply(safe_serialize)

        path = os.path.join(CSV_FOLDER, f"{table_name}.csv")
        df.to_csv(path, index=False)
        print(f"Экспортировано: {table_name} -> {path}")


def import_csv_to_database():
    """
    Импорт данных из CSV-файлов в базу.
    Очищаем таблицы перед загрузкой и десериализуем JSON-/ARRAY-столбцы.
    """
    metadata.reflect(bind=engine)

    with engine.begin() as conn:
        for table_name, table in metadata.tables.items():
            path = os.path.join(CSV_FOLDER, f"{table_name}.csv")
            if not os.path.exists(path):
                print(f"Пропущено (нет файла): {table_name}")
                continue

            # Очищаем таблицу
            conn.execute(text(f"DELETE FROM {table_name}"))

            # Загружаем CSV
            df = pd.read_csv(path)

            # Определяем JSON- и ARRAY-столбцы
            json_cols = [col.name for col in table.columns
                         if isinstance(col.type, (JSON, JSONB, ARRAY))]

            # Десериализуем JSON-строки обратно в объекты Python
            for col in json_cols:
                df[col] = df[col].apply(safe_deserialize)

            # Подготавливаем данные к вставке
            records = df.where(pd.notnull(df), None).to_dict(orient='records')

            # Вставляем через SQLAlchemy Core, чтобы адаптация типов работала корректно
            conn.execute(table.insert(), records)
            print(f"Импортировано: {table_name} из {path}")



#export_database_to_csv()
import_csv_to_database()
