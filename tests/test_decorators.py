import os.path
import re

import pytest

from src.decorators import log, print_message


def test_print_message_to_console(capsys):
    print_message(None, 'test_message')
    captured = capsys.readouterr()
    assert captured.out == 'test_message\n'


def test_print_message_to_file():
    # Записываем 2 сообщения в файл test_log.txt
    print_message('test_log.txt', 'First_message')
    print_message('test_log.txt', 'Second_message')

    current_dir = os.path.dirname(__file__)  # Папка, где лежит модуль
    test_file = os.path.join(current_dir, '../logs/test_log.txt')  # Абсолютный путь к файлу

    with open(test_file, encoding='utf-8') as f:
        content = f.read().splitlines()
    os.remove(test_file)

    assert content == ['First_message', 'Second_message']


def test_log_console(capsys):
    @log()
    def division(a, b):
        return a / b

    # функция отрабатывает без вызова ошибки
    division(10, 2)
    captured = capsys.readouterr()
    start_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} division started with args: \(10, 2\) and kwargs: \{\}"
    end_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} division finished successfully with result: 5"
    assert re.search(start_pattern, captured.out)
    assert re.search(end_pattern, captured.out)

    # функция отрабатывает с вызовом ошибки
    with pytest.raises(ZeroDivisionError):
        division(10, 0)
    captured = capsys.readouterr()
    assert ('division started with args: (10, 0) and kwargs: {}' in captured.out
            and 'division error: division by zero. Inputs: (10, 0), {}' in captured.out)
