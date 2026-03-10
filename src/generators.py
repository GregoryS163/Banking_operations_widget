from typing import Generator, Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator:
    """
    :param transactions: список словарей с транзакциями
    :param currency: заданная валюта
    :return: итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной
    """
    if isinstance(transactions, list) and all(isinstance(item, dict) for item in transactions):
        return (
            t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code", None) == currency
        )
    else:
        raise TypeError('Ожидается список словарей')


def transaction_descriptions(transactions: list[dict]) -> Generator:
    """
    :param transactions: список словарей с транзакциями
    :return: возвращает описание каждой операции по очереди
    """
    if isinstance(transactions, list) and all(isinstance(item, dict) for item in transactions):
        for t in transactions:
            yield t.get("description")
    else:
        raise TypeError('Ожидается список словарей')


def card_number_generator(start: int | str, stop: int | str) -> Generator:
    """
    Генератор карт, который выдает номера банковских карт.
    Генератор может сгенерировать номера карт в заданном диапазоне
    от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    :param start: начальное значения для генерации диапазона номеров
    :param stop: конечное значения для генерации диапазона номеров
    :return: номер карты в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    """
    start_int = int(start)
    stop_int = int(stop)

    min_val = 1
    max_val = 10 ** 16 - 1
    if start_int < min_val or stop_int > max_val:
        raise ValueError(f'The valid range of numbers is from {min_val} to {max_val}')
    if start_int > stop_int:
        raise ValueError('start must be <= stop')
    for num in range(start_int, stop_int + 1):
        number = str(num).zfill(16)
        formatted_number = f"{number[:4]} {number[4:8]} {number[8:12]} {number[12:]}"
        yield formatted_number
