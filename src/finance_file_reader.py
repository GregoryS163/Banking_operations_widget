import pandas as pd


def read_csv_transactions(path: str) -> list[dict]:
    df = pd.read_csv(path, delimiter=';')
    return df.to_dict(orient='records')


def read_excel_transactions(path: str) -> list[dict]:
    df = pd.read_excel(path)
    return df.to_dict(orient='records')
