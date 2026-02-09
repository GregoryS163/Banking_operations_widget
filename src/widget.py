import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_scor: str) -> str:
    """
    Обрабатывает информацию о картах, и о счетах.
    :param card_or_scor: Принимать один аргумент — строку,
    содержащую тип и номер карты или счета,
    :return: возвращать строку с замаскированным номером.
    """
    if re.match(r"Сч", card_or_scor):
        score_number = int(card_or_scor.split()[-1])
        mask_account = get_mask_account(score_number)
        return f'Счет {mask_account}'

    else:
        card_number_list = card_or_scor.split()
        card_number = int(card_number_list[-1])
        mask_card_number = get_mask_card_number(card_number)
        if len(card_number_list) == 3:
            return f'{card_number_list[0]} {card_number_list[1]} {mask_card_number}'
        else:
            return f'{card_number_list[0]} {mask_card_number}'


def get_date(date_information: str) -> str:
    """
    Преобразует формат даты,
    :param date_information: принимает на вход строку с датой в формате
    '2024-03-11T02:26:18.671407'
    :return: возвращает строку с датой в формате 'ДД.ММ.ГГГГ' ('11.03.2024')
    """
    # Получение всех групп в виде кортежа
    date_pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    match = re.search(date_pattern, date_information)
    if match:
        year, month, day = match.groups()
    return f"{day}.{month}.{year}"
