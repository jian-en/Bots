import time
import json
import requests
import datetime

import sender

RAW = """Host: ais.usvisa-info.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: application/json, text/javascript, */*; q=0.01
X-CSRF-Token: Hp2bSpgcKoVWEfWJss/igtB9lNvVu9Q/EPhkYagsDfaONr1KuxuB+5kTd4YTOfW8eEqhzv8UueZyizdEBtUwLg==
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Referer: https://ais.usvisa-info.com/en-MX/niv/schedule/29831778/appointment
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9"""

url = "https://ais.usvisa-info.com/en-MX/niv/schedule/29831778/appointment/days/74.json"
payload = {'appointments[expedite]': 'false'}

LO_BOUND = datetime.date(2019, 12, 9)
HI_BOUND = datetime.date(2019, 12, 20)

def build_request(c_data):
    headers = {}
    for line in RAW.split('\n'):
        key, value = [item.strip() for item in line.split(':', 1)]
        headers[key] = value
    r = requests.get(url, 
                     params=payload, 
                     cookies={'_yatri_session': c_data}, 
                     headers=headers)
    return r.json(), r.cookies['_yatri_session']

def in_range(d):
    return d >= LO_BOUND and d <= HI_BOUND

def get_data():
    with open("cookie", "r") as f:
        cookie_data = f.read().strip()

    result, new_cookie_data = build_request(cookie_data)
    available_slots = []
    for item in result:
        d_str, is_available = item["date"], item["business_day"]
        d = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
        if is_available and in_range(d):
            available_slots.append(d)

    with open("cookie", "w") as f:
        f.write(new_cookie_data)

    if len(available_slots) > 0:
        print('need to send...')
        sender.send_to_topic(','.join([slot.strftime("%Y-%m-%d") for slot in available_slots]))

if __name__ == '__main__':
    get_data()
