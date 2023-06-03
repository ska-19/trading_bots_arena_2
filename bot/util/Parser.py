import os
import requests
import json
import pandas as pd
from binance.client import Client
from django.http import HttpRequest


class Parser:
    def __init__(self, api_key=None, api_secret=None):
        if api_key is None and api_secret is None:
            os.environ['BINANCE_API_KEY_TEST'] = 'pzmgidTR4ZkCpdYkkj1YtpFkvWpwy8Z8IT3lhP51oQRrEl1lbgZbDnTKTTRj1IpL'
            os.environ['BINANCE_API_SECRET_TEST'] = 'LJkqD4uPqnUzq23pPWjY1c3q6rqgDwSWt1n7u3fynNL4WtG7OvbJQVDJUdL5egiw'
            api_key = os.environ['BINANCE_API_KEY_TEST']
            api_secret = os.environ['BINANCE_API_SECRET_TEST']
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret, testnet=True)

    def get_tickers(self):
        return self.client.get_all_tickers()

    def get_coin_ticker(self, coin):
        url = 'https://api1.binance.com'
        api_call = '/api/v3/ticker/price'
        headers = {'content-type': 'application/json', 'X-MBX-APIKEY': self.api_key}
        params = {'symbol': coin}
        response = requests.get(url + api_call, params=params, headers=headers)
        response = json.loads(response.text)
        return response["price"]

    def get_coin_info(self, coin):
        return self.client.get_symbol_info(coin)


if __name__ == "__main__":
    parser = Parser()
    print(parser.get_tickers())
