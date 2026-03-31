import pandas as pd


def read_csv_transactions(path: str) -> list[dict]:
    """Читает транзакции из csv-файла и возвращает их в виде списка словарей."""
    df = pd.read_csv(path, delimiter=";")
    return df.to_dict(orient="records")


def read_excel_transactions(path: str) -> list[dict]:
    """Читает транзакции из Excel-файла и возвращает их в виде списка словарей."""
    df = pd.read_excel(path)
    return df.to_dict(orient="records")
