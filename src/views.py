from utils import greetings, cards, top_transactions, currency_rates, stock_prices
import json


def main_page(date):
    data = {
        "greeting": greetings(),
        "cards": cards(date),
        "top_transactions": top_transactions(date),
        "currency_rates": currency_rates(),
        "stock_prices": stock_prices()
    }
    json_data = json.dumps(data)
    return json_data

# print(main_page('20.05.2021'))
