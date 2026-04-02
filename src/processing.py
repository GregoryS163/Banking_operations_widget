import re
from collections import Counter
from typing import Iterator


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    :param transactions: принимает список словарей по типу:
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},...]
    :param state: значение для ключа 'state'
    :return: новый список словарей, содержащий только те словари, у которых ключ 'state'
        соответствует указанному значению
    """
    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: list[dict], reverse_order: bool = True) -> list[dict]:
    """
    :param transactions: список словарей по типу:
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'...},...]
        key=lambda x: datetime.strptime(x.get("date", 'ключ не найден'), "%Y-%m-%dT%H:%M:%S.%f")
    :param reverse_order: параметр, задающий порядок сортировки reverse
    :return: новый список, отсортированный по ключу 'date'
    """
    sorted_transactions = sorted(transactions, key=lambda x: x.get("date", 'ключ не найден'), reverse=reverse_order)
    return sorted_transactions


def process_bank_search(transactions: list[dict] | Iterator, search: str) -> list[dict]:
    """ Фильтрует банковские операции по категории операции с помощью строку для поиска
    :param transactions: список словарей с данными о банковских операциях
    :param search: строку для поиска
    :return: возвращает список словарей, у которых в описании есть данная строка.
    """
    pattern = rf'{search}'
    transactions_by_pattern = [
        transaction for transaction in transactions if
        re.search(pattern, str(transaction.get('description')), flags=re.IGNORECASE)
    ]
    return transactions_by_pattern


def process_bank_operations(transactions: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по категориям операций из description.
        :param transactions: Список транзакций
        :param categories: Список категорий операций
        :return: Словарь, в котором ключи — это названия категорий,
        а значения — это количество операций в каждой категории
    """
    return dict(Counter(
        next((
            cat for cat in categories
            if cat.lower() in str(t.get('description', '')).lower()
        ), None)
        for t in transactions
    ))
    # Альтернативный способ решения:
    # counter = Counter()
    # for transaction in transactions:
    #     for cat in categories:
    #         if cat.lower() in str(transaction.get('description', '')).lower():
    #             counter[cat] += 1
    #             break
    # return dict(counter)
