import json


def load_transactions(path: str) -> list:
    """
    Читает JSON‑файл с транзакциями и возвращает список словарей(транзакций).
    Если файл пуст, не является списком или не найден — возвращает пустой список.
    """
    try:
        with open(path, encoding="utf-8") as f:
            transactions = json.load(f)
            return transactions if isinstance(transactions, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
