def get_mask_card_number(card_number: int) -> str:
    """accepts the card number as a number and returns the number mask according to the rule
    XXXX XX** **** XXXX"""
    c_num_str = str(card_number)
    return f"{c_num_str[0:5]} {c_num_str[5:7]}** **** {c_num_str[-4:]}"


def get_mask_account(account_number: int) -> str:
    """принимает на вход номер счета в виде числа и возвращает маску номера по правилу
    **XXXX"""
    account_number_str = str(account_number)
    return f"**{account_number_str[-4:]}"
