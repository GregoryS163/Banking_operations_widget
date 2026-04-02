from datetime import datetime
from typing import Generator

from settings import CSV_RATH, JSON_RATH, XLSX_RATH
from src.finance_file_reader import read_csv_transactions, read_excel_transactions
from src.generators import transaction_descriptions
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_transactions
from src.widget import mask_account_card

if __name__ == "__main__":
    print("""Привет! Добро пожаловать в программу работы с банковскими транзакциями.""")
    file_type = input("""Выберите необходимый пункт меню (1/2/3):
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла\n""")
    file_type_dict = {"1": "JSON", "2": "CSV", "3": "XLSX"}
    print(f"Для обработки выбран {file_type_dict[file_type]}-файл")

    file_reader = {
        "1": load_transactions(JSON_RATH),
        "2": read_csv_transactions(CSV_RATH),
        "3": read_excel_transactions(XLSX_RATH),
    }
    transactions = file_reader[file_type]

    states = "EXECUTED, CANCELED, PENDING"
    while True:
        transaction_state = input(f"""Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: {states}\n""").upper().strip()
        if transaction_state in states:
            break
        else:
            print(f'Статус операции "{transaction_state}" недоступен.')

    transactions: list[dict] = filter_by_state(transactions, transaction_state)
    print(f'Операции отфильтрованы по статусу "{transaction_state}"')

    sort_date = input("Отсортировать операции по дате? Да/Нет\n").lower().strip()
    if sort_date == "да":
        sort_direction = (
            input("\nОтсортировать по возрастанию или по убыванию? по возрастанию/по убыванию\n").lower().strip()
        )
        if reverse_order := sort_direction == "по убыванию":
            transactions = sort_by_date(transactions, reverse_order)

    only_rub = input("\nВыводить только рублевые транзакции? Да/Нет\n").lower().strip()
    if only_rub == "да":
        if file_type == "1":
            transactions = [t for t in transactions if t["operationAmount"]["currency"]["code"]]
        else:
            transactions = [t for t in transactions if t["currency_code"] == "RUB"]

    filter_by_keyword = (
        input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").lower().strip()
    )
    if filter_by_keyword == "да":
        keyword = input("\nВведите ключевое слово для фильтрации\n").strip()
        transactions: list[dict] = process_bank_search(transactions, keyword)

    if transactions:
        print("Распечатываю итоговый список транзакций...\n")
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")

        descriptions: Generator = transaction_descriptions(transactions)
        for t in transactions:
            if file_type == "1":
                amount = f"{t['operationAmount']['amount']}"
                currency_code = f"{t['operationAmount']['currency']['code']}"
                date_t = datetime.strptime(t.get("date"), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
            else:
                amount = f"{t['amount']}"
                currency_code: str = t['currency_code']
                date_t: str = datetime.strptime(t.get("date"), "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")

            print(f"{date_t} {next(descriptions)}")

            if t.get("description") == "Открытие вклада" and not isinstance(t["to"], float):
                print(mask_account_card(t["to"]))
            elif not isinstance(t["from"], float) and not isinstance(t["to"], float):
                print(f"{mask_account_card(t["from"])} -> {mask_account_card(t["to"])}")

            print(f"Сумма: {amount} {currency_code}\n")
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
