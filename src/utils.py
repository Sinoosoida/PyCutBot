import os
import time


def change_ext(path, new_ext):
    return os.path.splitext(path)[0] + new_ext


def fix_filename(filename: str):
    fixed_filename = filename.replace(" ", "_")
    print(f"FIXING FILENAME: {filename} to {fixed_filename}")
    os.rename(filename, fixed_filename)
    return fixed_filename


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        name = func.__name__.upper()
        print(f"{name} TIME: {end - start}")
        return func_return_val

    return wrapper


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
