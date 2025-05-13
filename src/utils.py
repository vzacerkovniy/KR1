from datetime import datetime as dt, timedelta
from dotenv import load_dotenv
import pandas as pd
import requests
import json

now = dt.now()
load_dotenv()

def greetings():
    '''Функция приветствия'''
    if now.hour > 4 and now.hour <= 12:
        return 'Доброе утро'
    if now.hour > 12 and now.hour <= 16:
        return 'Добрый день'
    if now.hour > 16 and now.hour <= 24:
        return 'Добрый вечер'
    if now.hour >= 0 and now.hour <= 4:
        return 'Доброй ночи'


def cards(user_date):
    '''Функция выдающая данные по использованным картам за период времени'''
    data = pd.read_excel('../data/operations.xlsx')
    end_date = dt.strptime(user_date, '%d.%m.%Y')
    start_date = end_date.replace(day=1)
    data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], dayfirst=True)
    filt_data = data[(data['Дата платежа'].between(start_date, end_date))]
    filt_data['Дата платежа'] = filt_data['Дата платежа'].dt.strftime('%d.%m.%Y')
    card_list = filt_data['Номер карты'].unique().tolist()
    cards = []
    for card in card_list[:-1]:
        card_data = filt_data[filt_data['Номер карты'] == card]
        card_num = card[1:]
        total_sum = float(round(card_data['Сумма операции с округлением'].sum(), 2))
        cash = round(total_sum // 100, 2)
        card_data = {"last_digits": card_num, "total_spent": total_sum, "cashback": cash}
        cards.append(card_data)
    return cards


def top_transactions(user_date):
    data = pd.read_excel('../data/operations.xlsx')
    end_date = dt.strptime(user_date, '%d.%m.%Y')
    start_date = end_date.replace(day=1)
    data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], dayfirst=True)
    filt_data = data[(data['Дата платежа'].between(start_date, end_date))]
    filt_data['Дата платежа'] = filt_data['Дата платежа'].dt.strftime('%d.%m.%Y')
    sorted_data = filt_data.sort_values(by='Сумма операции с округлением', ascending=False).reset_index()
    top_data = sorted_data.iloc[:5]
    transactions = [{"date": top_data['Дата платежа'][0],
                     "amount": float(top_data['Сумма операции с округлением'][0]),
                     "category": top_data['Категория'][0],
                     "description": top_data['Описание'][0]},
                     {"date": top_data['Дата платежа'][1],
                     "amount": float(top_data['Сумма операции с округлением'][1]),
                     "category": top_data['Категория'][1],
                     "description": top_data['Описание'][1]},
                     {"date": top_data['Дата платежа'][2],
                     "amount": float(top_data['Сумма операции с округлением'][2]),
                     "category": top_data['Категория'][2],
                     "description": top_data['Описание'][2]},
                     {"date": top_data['Дата платежа'][3],
                     "amount": float(top_data['Сумма операции с округлением'][3]),
                     "category": top_data['Категория'][3],
                     "description": top_data['Описание'][3]},
                     {"date": top_data['Дата платежа'][4],
                     "amount": float(top_data['Сумма операции с округлением'][4]),
                     "category": top_data['Категория'][4],
                     "description": top_data['Описание'][4]}
    ]
    return transactions


def currency_rates():
    with open('../user_settings.json') as f:
        settings = json.load(f)['user_currencies']
    rates = []
    # print(settings)
    for i in settings:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={i}"
        payload = {}
        headers = {
            "apikey": "OvJuc7ilkG92inHXXwRjYAjBx1SqHAFx"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.text
        parsed_result = json.loads(result)
        # status_code = response.status_code
        # print(status_code)
        # print(result)
        rates.append({"currency": parsed_result["base"], "rate": parsed_result["rates"]["RUB"]})

    return rates


def stock_prices():
    now_day = (dt.now().date() - timedelta(1)).strftime('%Y-%m-%d')
    with open('../user_settings.json') as f:
        settings = json.load(f)['user_stocks']
    stocks = []
    for i in settings:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={i}&apikey=VNIETXDIJH5KHBDT"
        response = requests.get(url)
        result = response.text
        # print(result)
        parsed_result = json.loads(result)
        stocks.append({"stock": parsed_result["Meta Data"]["2. Symbol"], "price": parsed_result["Time Series (Daily)"][now_day]['1. open']})

    return stocks
