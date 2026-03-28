import pytest
import json
from unittest.mock import patch, mock_open

from src.utils import load_transactions


# Тест успешной загрузки списка транзакций
def test_load_transactions_valid_json():
    transactions = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    json_content = json.dumps(transactions)

    with patch("builtins.open", mock_open(read_data=json_content)):
        result = load_transactions("test.json")

    assert result == transactions


# Тест пустого JSON файла
# Тест невалидного JSON (не список)
# Тест поврежденного JSON
# Тест пустого файла
# Во всех случаях должен возвращаться пустой список
@pytest.mark.parametrize("read_data", ["[]", '{"key": "value"}', "{invalid json", ""])
def test_load_transactions_empty_file(read_data):
    with patch("builtins.open", mock_open(read_data=read_data)):
        result = load_transactions("test.json")

    assert result == []


# Тест несуществующего файла
def test_load_transactions_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("nonexistent.json")

    assert result == []
