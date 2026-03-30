from logging_config import setup_logging

logger = setup_logging(__name__)


def get_mask_card_number(card_number: int | str) -> str:
    """accepts the card number as a number and returns the number mask according to the rule
    XXXX XX** **** XXXX"""
    card_num_str = str(card_number)
    if len(card_num_str) != 16 or not card_num_str.isdigit():
        logger.error('Номер карты должен состоять из 16 цифр и быть переданным к виде числа или строки')
        raise ValueError('Номер карты должен состоять из 16 цифр и быть переданным к виде числа или строки')
    logger.info('Маска номера карты получена')
    return f"{card_num_str[0:4]} {card_num_str[4:6]}** **** {card_num_str[-4:]}"


def get_mask_account(account_number: int | str) -> str:
    """Принимает на вход номер счета в виде числа из 20 цифр и возвращает маску номера по правилу
    **XXXX"""
    account_number_str = str(account_number)
    if len(account_number_str) != 20 or not account_number_str.isdigit():
        logger.error('Номер счета должен состоять из 20 цифр и быть переданным к виде числа или строки')
        raise ValueError('Номер счета должен состоять из 20 цифр и быть переданным к виде числа или строки')
    logger.info('Маска номера счёта получена')
    return f"**{account_number_str[-4:]}"
