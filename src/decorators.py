import os.path
from functools import wraps
from time import localtime, strftime
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")  # Тип возвращаемого значения
P = ParamSpec("P")  # Параметры функции


def print_message(filename: str | None, text_message: str) -> None:
    """Вспомогательная функция для записи лога в файл или вывода в консоль"""
    if filename is None:
        print(text_message)
    else:
        current_dir = os.path.dirname(__file__)  # Папка, где лежит модуль
        log_path = os.path.join(current_dir, "../logs/" + filename)  # Абсолютный путь к файлу
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{text_message}\n")


def log(filename: str | None = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Декоратор, котрый логирует начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки"""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            log_text_start = (
                f"{strftime('%Y-%m-%d %H:%M:%S', localtime())} "
                f"{func.__name__} started with args: {args} and kwargs: {kwargs}"
            )
            print_message(filename, log_text_start)
            try:
                result = func(*args, **kwargs)
                lod_text_end = (
                    f"{strftime('%Y-%m-%d %H:%M:%S', localtime())} "
                    f"{func.__name__} finished successfully "
                    f"with result: {result}\n"
                )
                print_message(filename, lod_text_end)
                return result
            except Exception as e:
                lod_text_end = (
                    f"{strftime('%Y-%m-%d %H:%M:%S', localtime())} "
                    f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}\n"
                )
                print_message(filename, lod_text_end)
                raise e

        return wrapper

    return decorator
