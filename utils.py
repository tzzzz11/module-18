import json
import requests
from config import TOKEN, keys

class ExchangeException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'Одинаковые валюты не конвертируются {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Ошибка в валюте {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Ошибка в валюте {quote}')

        try:
            amount = int(amount)
        except ValueError:
            raise ExchangeException(f'Ошибка в количестве {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]])
        return total_base
