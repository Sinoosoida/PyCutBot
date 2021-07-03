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
