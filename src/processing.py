from datetime import datetime


def filter_by_state(state_info: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    :param state_info: принимает список словарей по типу:
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},...]
    :param state: значение для ключа 'state'
    :return: новый список словарей, содержащий только те словари, у которых ключ 'state'
        соответствует указанному значению
    """
    return [item for item in state_info if item.get("state") == state]


def sort_by_date(transactions: list[dict], reverse_order: bool = True) -> list[dict]:
    """
    :param transactions: список словарей по типу:
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},...]
    :param reverse_order: параметр, задающий порядок сортировки reverse
    :return: новый список, отсортированный по ключу 'date'
    """
    sorted_transactions = sorted(
        transactions, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=reverse_order
    )
    return sorted_transactions
