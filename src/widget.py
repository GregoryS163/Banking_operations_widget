from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account: str) -> str:
    """
    Обрабатывает информацию о картах, и о счетах.
    :param card_or_account: Строка, содержащая тип и номер карты или счета,
    :return: возвращает строку с замаскированным номером карты или счета.
    """
    if not isinstance(card_or_account, str):
        raise TypeError("Неверный тип данных")

    card_or_account_list = card_or_account.split()

    if card_or_account.startswith(("Счёт", "Счет")) and len(card_or_account_list) == 2:
        account_number = card_or_account_list[-1]
        mask_account = get_mask_account(account_number)
        return f"{card_or_account_list[0]} {mask_account}"

    elif card_or_account.startswith(
        (
            "МИР",
            "American Express",
            "Discover",
            "Maestro",
            "MasterCard",
            "Mastercard",
            "Visa",
            "Visa Classic",
            "Visa Platinum",
            "Visa Gold",
        )
    ):
        card_number = card_or_account_list[-1]
        mask_card_number = get_mask_card_number(card_number)
        if len(card_or_account_list) == 3:
            return f"{card_or_account_list[0]} {card_or_account_list[1]} {mask_card_number}"
        elif len(card_or_account_list) == 2:
            return f"{card_or_account_list[0]} {mask_card_number}"
    else:
        raise ValueError("Неверный формат карты или счёта")


def get_date(date_info: str) -> str:
    """
    Преобразует формат даты,
    :param date_info: принимает на вход строку с датой в формате
    '2024-03-11T02:26:18.671407'
    :return: возвращает строку с датой в формате 'ДД.ММ.ГГГГ' ('11.03.2024')
    """
    if not isinstance(date_info, str):
        raise TypeError("Неверный тип данных")
    parsed_datetime = datetime.strptime(date_info, "%Y-%m-%dT%H:%M:%S.%f")
    return parsed_datetime.strftime("%d.%m.%Y")
