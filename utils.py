import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        name = func.__name__.upper()
        print(f'{name} TIME: {end - start}')
        return func_return_val

    return wrapper


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
