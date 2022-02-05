import requests
import os
import time
import json

API_URL = "https://api.ssllabs.com/api/v2/analyze"
WAIT_TIME=10  # secs
HOST = "www.mwam.com"

def fetch(params):
    resp = requests.get(API_URL, params=params)
    if resp.status_code != 200:
        raise Exception(f"Error code: {resp.status_code}")
    return resp.json()

def main(url):
    params = {
        "host": url,
        "all": "done",  # full information will be returned only if the assessment is complete
        "startNew": "on"  # cached assessment results are ignored and a new assessment is started; to be used only the first time
    }
    res = fetch(params)
    del params["startNew"]

    while res["status"] != "ERROR" and res["status"] != "READY":
        print(f"status: {res['status']}; retrying in {WAIT_TIME} sec..")
        time.sleep(WAIT_TIME)
        res = fetch(params)
    return res

res = main(HOST)
print(json.dumps(res, indent=4, sort_keys=True))
