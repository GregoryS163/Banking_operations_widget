import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY not set in .env file")


def get_transaction_amount_rub(transaction: dict) -> float:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции в рублях.
     Если транзакция была в USD или EUR, происходит обращение к внешнему API
     для получения текущего курса валют и конвертации суммы операции в рубли
    """
    if not isinstance(transaction, dict):
        raise ValueError("transaction должен быть dict")

    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code", None)
    if currency_code is None or not isinstance(currency_code, str) or len(currency_code) != 3:
        raise ValueError("Invalid currency code")

    amount = transaction.get("operationAmount", {}).get("amount", None)
    if not amount or amount is None or not isinstance(amount, (str, int, float)) or float(amount) <= 0:
        raise ValueError("Invalid amount")

    if currency_code == "RUB":
        return float(amount)
    else:
        return round(conversion_amount_to_rub(currency_code, "RUB", amount), 2)


def conversion_amount_to_rub(from_: str, to_: str, amount: str) -> float:
    """
    Accesses an external API for currency conversion.
    :param from_: The three-letter currency code of the currency you would like to convert from.
    :param to_: The three-letter currency code of the currency you would like to convert to.
    :param amount: The amount to be converted.
    :param max_retries: the maximum number of connection attempts.
    :return: the amount in the specified currency.
    """
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_}&from={from_}&amount={amount}"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Автоматически raise HTTPError при 4XX/5XX
        return float(response.json()["result"])
    except (requests.exceptions.RequestException, ValueError) as e:
        raise RuntimeError(f"Currency conversion failed: {e}")
