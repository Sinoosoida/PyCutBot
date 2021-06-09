import requests


def get_request_with_retries(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        res = requests.get(url)
        if res.status_code == 200:
            return res
        retries += 1
