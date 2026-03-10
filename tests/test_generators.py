import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(transactions_for_gen, transactions_usd):
    assert list(filter_by_currency(transactions_for_gen, "USD")) == transactions_usd


def test_filter_by_currency_rub(transactions_for_gen, transactions_rub):
    assert list(filter_by_currency(transactions_for_gen, "RUB")) == transactions_rub


def test_filter_by_currency_no_currency(transactions_for_gen):
    assert list(filter_by_currency(transactions_for_gen, "KZT")) == []
    assert list(filter_by_currency([], "USD")) == []


@pytest.mark.parametrize(
    "transactions, currency", [("", "USD"), ("some text", "USD"), ({"one": 1}, "USD"), (1, "USD"), ((1,), "USD")]
)
def test_filter_by_currency_invalid_arg(transactions, currency):
    with pytest.raises(TypeError) as invalid_arg:
        filter_by_currency(transactions, currency)
    assert str(invalid_arg.value) == "Ожидается список словарей"


def test_transaction_descriptions(transactions_for_gen):
    generator = transaction_descriptions(transactions_for_gen)
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"


def test_transaction_descriptions_empty_list():
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    "transactions",
    ["", "some text", {"one": 1}, 1, (1,)],
)
def test_transaction_descriptions_invalid_arg(transactions):
    with pytest.raises(TypeError) as invalid_arg:
        generator = transaction_descriptions(transactions)
        next(generator)
    assert str(invalid_arg.value) == "Ожидается список словарей"


@pytest.mark.parametrize(
    "start, stop, expected_cards",
    [
        # разные диапазоны
        (500, 502, ["0000 0000 0000 0500", "0000 0000 0000 0501", "0000 0000 0000 0502"]),
        (10, 11, ["0000 0000 0000 0010", "0000 0000 0000 0011"]),
        # Крайние значения
        (1, 1, ["0000 0000 0000 0001"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        # Строка → int
        ("10", "12", ["0000 0000 0000 0010", "0000 0000 0000 0011", "0000 0000 0000 0012"]),
    ],
)
def test_card_generator_range(start, stop, expected_cards):
    """Проверяет диапазон, количество элементов и правильные значения."""
    gen = card_number_generator(start, stop)
    cards = list(gen)

    assert len(cards) == len(expected_cards)
    assert cards == expected_cards


@pytest.mark.parametrize(
    "card",
    [
        "0000 0000 0000 0001",
        "1234 5678 9012 3456",
        "9999 9999 9999 9999",
    ],
)
def test_card_format(card):
    """Проверяет формат номера для разных примеров."""
    parts = card.split()
    assert len(parts) == 4
    assert len(card) == 19
    for part in parts:
        assert len(part) == 4
        assert part.isdigit()


@pytest.mark.parametrize(
    "start, stop, error_msg_pattern",
    [
        (10, 5, "start must be <= stop"),
        (0, 5, "The valid range of numbers is from 1 to 9999999999999999"),
        (1, 10000000000000000, "The valid range of numbers is from 1 to 9999999999999999"),
    ],
)
def test_invalid_range(start, stop, error_msg_pattern):
    """Проверяет ValueError для невалидных диапазонов."""
    with pytest.raises(ValueError, match=error_msg_pattern):
        list(card_number_generator(start, stop))


@pytest.mark.parametrize(
    "start, stop, expected_first, expected_last",
    [
        (100, 105, "0000 0000 0000 0100", "0000 0000 0000 0105"),
        (9999999999999990, 9999999999999999, "9999 9999 9999 9990", "9999 9999 9999 9999"),
    ],
)
def test_generator_completion(start, stop, expected_first, expected_last):
    """Проверяет, что генератор начинается с first и заканчивается на last."""
    gen = card_number_generator(start, stop)
    cards = list(gen)

    assert len(cards) == (int(stop) - int(start) + 1)
    assert cards[0] == expected_first
    assert cards[-1] == expected_last

    # Генератор завершается (не бесконечный)
    assert len(cards) == (int(stop) - int(start) + 1)
