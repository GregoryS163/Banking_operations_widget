import pathlib

ROOT_PATH = pathlib.Path(__file__).parent
JSON_RATH = ROOT_PATH.joinpath('data', 'operations.json')
CSV_RATH = ROOT_PATH.joinpath('data', 'transactions.csv')
XLSX_RATH = ROOT_PATH.joinpath('data', 'transactions_excel.xlsx')
