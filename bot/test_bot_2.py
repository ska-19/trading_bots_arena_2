import requests
import json
import time

token = "1.31.11ZiKyjmcLFEcHyYQSwWaVRiyvryIM"

data_BNBBUSD = {
    "token": token,
    "token_id": "BNBBUSD",
    "amount": 4
}
data_ETHBUSD = {
    "token": token,
    "token_id": "ETHBUSD",
    "amount": 1
}
data_BTCBUSD = {
    "token": token,
    "token_id": "BTCBUSD",
    "amount": 1
}
js_1 = json.dumps(data_BNBBUSD)
js_2 = json.dumps(data_ETHBUSD)
js_3 = json.dumps(data_BTCBUSD)

flag_1 = True
flag_2 = False
flag_3 = False
while True:
    response = None
    if flag_1:
        response = requests.post("http://127.0.0.1:8000/api/botlist/buy/", json=data_BNBBUSD)
        flag_1, flag_2, flag_3 = False, True, False
    elif flag_2:
        response = requests.post("http://127.0.0.1:8000/api/botlist/buy/", json=data_ETHBUSD)
        flag_1, flag_2, flag_3 = False, False, True
    elif flag_3:
        response = requests.post("http://127.0.0.1:8000/api/botlist/buy/", json=data_BTCBUSD)
        flag_1, flag_2, flag_3 = False, False, False
    else:
        response = requests.post("http://127.0.0.1:8000/api/botlist/sell/", json=data_BNBBUSD)
        print(response.text)
        time.sleep(5)
        response = requests.post("http://127.0.0.1:8000/api/botlist/sell/", json=data_ETHBUSD)
        print(response.text)
        time.sleep(5)
        response = requests.post("http://127.0.0.1:8000/api/botlist/sell/", json=data_BTCBUSD)
        flag_1, flag_2, flag_3 = True, False, False
    print(response.text)
    time.sleep(5)