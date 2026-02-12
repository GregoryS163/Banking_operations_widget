def filter_by_state(state_info: list[dict], state='EXECUTED') -> list[dict]:
    """
    :param state_info: принимает список словарей по типу:
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},...]
    :param state: значение для ключа 'state'
    :return: новый список словарей, содержащий только те словари, у которых ключ 'state'
        соответствует указанному значению
        """
    return [item for item in state_info if item['state'] == state]


def sort_by_date(date_info: list[dict], reverse=True) -> list[dict]:
    pass
