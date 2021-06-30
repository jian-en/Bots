import requests
import datetime

RAW = """Host: ais.usvisa-info.com
Connection: keep-alive
sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
Accept: application/json, text/javascript, */*; q=0.01
X-CSRF-Token: Tnsxm71uPGSyjLhS7NpX1nNzVzGYBUffsnnvhl4W/BGfbquF+v+45qVT1jXCKo1RbNh6hxfZ6pZWZtAoH+AfFQ==
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
X-Requested-With: XMLHttpRequest
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ais.usvisa-info.com/en-gb/niv/schedule/33666589/appointment
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9"""

url = "https://ais.usvisa-info.com/en-gb/niv/schedule/33666589/appointment/days/17.json"
payload = {'appointments[expedite]': 'false'}

LO_BOUND = datetime.date(2021, 7, 1)
TA_DATE = datetime.date(2021, 7, 14)
HI_BOUND = datetime.date(2021, 7, 31)

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
    target_hit = False
    for item in result:
        d_str, is_available = item["date"], item["business_day"]
        d = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
        if target_hit is False:
            target_hit = d == TA_DATE

        if is_available and in_range(d):
            available_slots.append(d)

    with open("cookie", "w") as f:
        f.write(new_cookie_data)
    print(available_slots)
    print(target_hit)


if __name__ == '__main__':
    get_data()
