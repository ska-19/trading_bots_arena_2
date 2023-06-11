import requests
import json
import time

token = "1.30.wMud1ixrjOF9l7X13So1MzwlTV7t8a"

data = {
    "token": token,
    "token_id": "BNBBUSD",
    "amount": 1
}
js = json.dumps(data)
flag = True
while True:
    response = None
    if flag:
        response = requests.post("http://127.0.0.1:8000/api/botlist/buy/", json=data)
        flag = False
    else:
        response = requests.post("http://127.0.0.1:8000/api/botlist/sell/", json=data)
        flag = True
    print(response.text)
    time.sleep(10)