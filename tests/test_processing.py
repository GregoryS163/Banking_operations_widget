import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations


def test_filter_by_state(transactions, transactions_executed):
    assert filter_by_state(transactions) == transactions_executed


def test_filter_by_state_canceled(transactions, transactions_canceled):
    assert filter_by_state(transactions, state="CANCELED") == transactions_canceled


@pytest.mark.parametrize(
    "transactions",
    [
        [{"id": 1}],
        [{"id": 2, "state": 123}],
        [{"id": 3, "state": None}],
        [{"id": 4, "state": "another_text"}],
    ],
)
def test_filter_by_state_invalid_state(transactions):
    assert filter_by_state(transactions) == []


def test_sort_by_date(transactions, sorted_by_date):
    assert sort_by_date(transactions) == sorted_by_date


def test_sort_by_date_rev_false(transactions, sorted_by_date_reverse_false):
    assert sort_by_date(transactions, reverse_order=False) == sorted_by_date_reverse_false


# @pytest.mark.parametrize(
#     "transactions",
#     [
#         [{"date": "2026-02-21 16:43:51.909117"}],
#         [{"date": "2026/02/21"}],
#         [{"date": "30-01-2026T00:00:00.000000"}],
#         [{"date": "21.02.2026"}],
#         [{"date": ""}],
#     ],
# )
# def test_get_date_invalid_date(transactions):
#     with pytest.raises(ValueError):
#         sort_by_date(transactions)


# -----Тесты для process_bank_search---
def test_process_bank_search(sample_transactions, sample_transactions_executed, ):
    result = process_bank_search(sample_transactions, 'перевод')
    assert result == sample_transactions_executed


# -----Тесты для process_bank_operations---
def test_process_bank_operations(sample_transactions):
    categories = ['Перевод организации', 'Перевод с карты на карту', 'Открытие вклада']
    result = process_bank_operations(sample_transactions, categories)
    assert result == {'Перевод организации': 1, 'Перевод с карты на карту': 2, 'Открытие вклада': 1}
