import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "card_or_account, expected_result",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card(card_or_account, expected_result):
    assert mask_account_card(card_or_account) == expected_result


@pytest.mark.parametrize(
    "card_or_account",
    [
        {"Счет 64686473678894779589"},
        ["Visa Classic 6831982476737658"],
        1111222233334444,
    ],
)
def test_mask_account_card_invalid_type_arg(card_or_account):
    with pytest.raises(TypeError) as invalid_type_arg:
        assert mask_account_card(card_or_account)
    assert str(invalid_type_arg.value) == "Неверный тип данных"


@pytest.mark.parametrize(
    "card_or_account",
    [
        "Счет 0123456789",
        "1111222233334444",
        "Visa Visa 1111222233334444",
        "Some_text some_text 1111222233334444",
        "Some_text",
        "MasterCard 71583007",
    ],
)
def test_mask_account_card_invalid_arg(card_or_account):
    with pytest.raises(ValueError) as invalid_arg:
        mask_account_card(card_or_account)
    assert (
        str(invalid_arg.value) == "Неверный формат карты или счёта"
        or "Номер карты должен состоять из 16 цифр"
        or "Номер счета должен состоять из 20 цифр"
    )


@pytest.mark.parametrize(
    "date_info, expected_result",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2026-01-30T00:00:00.000000", "30.01.2026"),
    ],
)
def test_get_date(date_info, expected_result):
    assert get_date(date_info) == expected_result


@pytest.mark.parametrize(
    "date_info",
    [
        ["2026-01-30T00:00:00.000000"],
        {"2026-01-30T00:00:00.000000"},
        ("2026-01-30T00:00:00.000000",),
        20260130000000000000,
    ],
)
def test_get_date_invalid_type_arg(date_info):
    with pytest.raises(TypeError) as invalid_type_arg:
        get_date(date_info)
    assert str(invalid_type_arg.value) == "Неверный тип данных"


@pytest.mark.parametrize(
    "date_info", ["2026-02-21 16:43:51.909117", "2026-02-21", "30-01-2026T00:00:00.000000", "21-02-2026", ""]
)
def test_get_date_invalid_arg(date_info):
    with pytest.raises(ValueError):
        get_date(date_info)
