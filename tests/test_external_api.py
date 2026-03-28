import json
import pytest
from unittest.mock import patch, Mock

from src.external_api import conversion_amount_to_rub, get_transaction_amount_rub


# ----- Тесты для get_transaction_amount_rub -----

def test_get_transaction_amount_rub_rub(rub_transaction):
    result = get_transaction_amount_rub(rub_transaction)
    assert isinstance(result, float)
    assert result == 1000.0


def test_get_transaction_amount_rub_not_dict():
    with pytest.raises(ValueError, match="transaction должен быть dict"):
        get_transaction_amount_rub("not a dict")


def test_conversion_amount_to_rub_usd(usd_transaction):
    with patch('src.external_api.conversion_amount_to_rub') as conversion_mock:
        conversion_mock.return_value = 500.123
        assert get_transaction_amount_rub(usd_transaction) == 500.12
        conversion_mock.assert_called_once_with('USD', 'RUB', '50')


def test_get_transaction_amount_rub_invalid_currency_code():
    bad = {"operationAmount": {"amount": "100", "currency": {"code": "xx"}}}
    with pytest.raises(ValueError, match="Invalid currency code"):
        get_transaction_amount_rub(bad)


def test_get_transaction_amount_rub_empty_currency_code():
    bad = {"operationAmount": {"amount": "100"}}
    with pytest.raises(ValueError, match="Invalid currency code"):
        get_transaction_amount_rub(bad)


@pytest.mark.parametrize(
    'transaction',
    [
        {"operationAmount": {"amount": "", "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": "-50", "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": "0", "currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
    ],
)
def test_get_transaction_amount_rub_invalid_amount(transaction):
    """
    invalid_amount_string_empty
    invalid_amount_negative
    invalid_amount_zero
    invalid_amount_none
    """
    with pytest.raises(ValueError, match="Invalid amount"):
        get_transaction_amount_rub(transaction)


# ----- Тесты для conversion_amount_to_rub -----

@patch('requests.get')
def test_conversion_amount_to_rub_success(mock_get):
    """Тест успешной конвертации валют."""
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": 123.45}

    result = conversion_amount_to_rub("USD", "RUB", "10")

    assert isinstance(result, float)
    assert result == 123.45
    mock_get.assert_called_once_with(
        'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10',
        headers={'apikey': 'skwzuto28qGcbr8bHQQDRoSOMwf2aDkP'}
    )


def test_conversion_amount_to_rub_invalid_json():
    """Тест обработки некорректного JSON ответа."""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(RuntimeError, match="Currency conversion failed: Invalid JSON"):
            conversion_amount_to_rub("USD", "RUB", "10")
