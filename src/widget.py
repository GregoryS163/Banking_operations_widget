import re

from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(card_or_scor: str) -> str:
    """
    Обрабатывает информацию о картах, и о счетах.
    :param card_or_scor: Принимать один аргумент — строку,
    содержащую тип и номер карты или счета,
    :return: возвращать строку с замаскированным номером.
    """
    if re.match(r"Сч", card_or_scor):
        score_number = int(card_or_scor.split()[-1])
        return get_mask_account(score_number)

    else:
        card_number = int(card_or_scor.split()[-1])
        return get_mask_card_number(card_number)

