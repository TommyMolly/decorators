import os
import datetime


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            function_name = old_function.__name__
            args_str = f"args: {args}, kwargs: {kwargs}"
            result = old_function(*args, **kwargs)
            log_message = (
                f"[{now}] Function '{function_name}' called with {args_str}. "
                f"Returned: {result}\n"
            )
            with open(path, "a") as log_file:
                log_file.write(log_message)
            return result
        return new_function
    return __logger


@logger("math_solver.log")
def discriminant(a, b, c):
    return b ** 2 - 4 * a * c

@logger("math_solver.log")
def solution(a, b, c):
    D = discriminant(a, b, c)

    if D < 0:
        print("корней нет")
        return "корней нет"
    elif D == 0:
        x = -b / (2 * a)
        print(x)
        return x
    else:
        x1 = (-b + D ** 0.5) / (2 * a)
        x2 = (-b - D ** 0.5) / (2 * a)
        print(x1, x2)
        return x1, x2


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger(path)
    def hello_world():
        return 'Hello World'

    @logger(path)
    def summator(a, b=0):
        return a + b

    @logger(path)
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    print("Тестирование уравнений:")
    solution(1, 8, 15)  # -3.0 -5.0
    solution(1, -13, 12)  # 12.0 1.0
    solution(-4, 28, -49)  # 3.5
    solution(1, 1, 1)  # корней нет

    print("\nЗапуск test_1:")
    test_1()

    print("\nЗапуск test_2:")
    test_2()
