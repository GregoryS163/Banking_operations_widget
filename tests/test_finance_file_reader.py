# import pytest
from unittest.mock import Mock, patch
import pandas as pd

from src.finance_file_reader import read_csv_transactions, read_excel_transactions


# Тесты для CSV
@patch('pandas.read_csv')
def test_read_csv_transactions_success(mock_read_csv, sample_csv_data):
    """Тест успешного чтения CSV."""
    mock_df = mock_read_csv.return_value
    # mock_df.to_dict.return_value = {'records': sample_csv_data}
    mock_df.to_dict.return_value = sample_csv_data  # orient='records'

    result = read_csv_transactions('test.csv')

    mock_read_csv.assert_called_once_with('test.csv', delimiter=';')
    mock_df.to_dict.assert_called_once_with(orient='records')
    assert result == sample_csv_data


@patch('pandas.read_csv')
def test_read_csv_transactions_empty(mock_read_csv):
    """Тест пустого CSV."""
    mock_df = mock_read_csv.return_value
    mock_df.to_dict.return_value = []

    result = read_csv_transactions('empty.csv')

    assert result == []


# Тесты для Excel

def test_read_excel_transactions_success(sample_csv_data):
    """Тест успешного чтения Excel."""
    mock_df = Mock()
    mock_df.to_dict.return_value = sample_csv_data

    with patch('pandas.read_excel', return_value=mock_df) as mock_read_excel:
        result = read_excel_transactions('test.xlsx')

    mock_read_excel.assert_called_once_with('test.xlsx')
    mock_df.to_dict.assert_called_once_with(orient='records')
    assert result == sample_csv_data


def test_read_excel_transactions_empty():
    """Тест пустого Excel."""
    mock_df = Mock()
    mock_df.to_dict.return_value = []

    with patch('pandas.read_excel', return_value=mock_df):
        result = read_excel_transactions('empty.xlsx')

    assert result == []
