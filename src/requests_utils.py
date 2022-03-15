from time import sleep

import requests


def get_request_with_retries(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        res = requests.get(url)
        if res.status_code == 200:
            return res
        retries += 1


def with_retries(max_retries=5, sleep_time=2):
    def wrap1(func):
        def wrap2(*args, **kwargs):
            for retry in range(max_retries):
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as ex:
                    print(f"Error executing {func.__name__}: {ex}", end="")
                    if retry < max_retries - 1:
                        print(", retrying")
                        sleep(sleep_time)
                    else:
                        print()
                        return None

        return wrap2

    return wrap1
