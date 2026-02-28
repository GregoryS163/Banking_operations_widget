import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected_result",
    [
        (1111222233334444, "1111 22** **** 4444"),
        (5555555555555555, "5555 55** **** 5555"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number(card_number, expected_result):
    assert get_mask_card_number(card_number) == expected_result


@pytest.mark.parametrize(
    "card_number",
    [
        11112222333344445,
        111122223333444,
        "aaaabbbbccccdddd",
        [1111222233334444],
        "",
    ],
)
def test_get_mask_card_number_invalid_arg(card_number):
    with pytest.raises(ValueError) as invalid_arg:
        get_mask_card_number(card_number)
    assert str(invalid_arg.value) == "Номер карты должен состоять из 16 цифр и быть переданным к виде числа или строки"


@pytest.mark.parametrize(
    "account_number, expected_result",
    [(11112222333344445555, "**5555"), (11111111111111111111, "**1111"), ("11112222333344440000", "**0000")],
)
def test_get_mask_account(account_number, expected_result):
    assert get_mask_account(account_number) == expected_result


@pytest.mark.parametrize(
    "account_number",
    [
        111122223333444455556,
        111122223334444555,
        "str of 20 characters",
        [11112222333344445555],
        "",
    ],
)
def test_get_mask_account_invalid_arg(account_number):
    with pytest.raises(ValueError) as invalid_arg:
        get_mask_account(account_number)
    assert str(invalid_arg.value) == "Номер счета должен состоять из 20 цифр и быть переданным к виде числа или строки"
