import json

from logging_config import setup_logging

logger = setup_logging(__name__)


def load_transactions(path: str) -> list:
    """
    Читает JSON‑файл с транзакциями и возвращает список словарей(транзакций).
    Если файл пуст, не является списком или не найден — возвращает пустой список.
    """
    try:
        with open(path, encoding='utf-8') as f:
            transactions = json.load(f)
            logger.info('Список транзакций загружен')
            return transactions if isinstance(transactions, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f'{e}')
        return []
