import time

import requests, json, datetime, os, telebot

CURRENCY_RATES_FILE = "currency_rates_eur.json"
BOT_TOKEN = os.getenv("TELEGRAM_KEY")
CHAT_ID = '5462477537'  #Мой бот
API_KEY = os.getenv("APILAYER_KEY")


def main():
    while True:
        currency = 'EUR'
        rate = get_currency_rate(currency)
        # print(rate)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = f"Курс {currency} к рублю: {rate:.2f}"
        print(result)
        date = {"currency": currency, "rate": rate, "timestamp": timestamp}
        date1 = load_from_json(CURRENCY_RATES_FILE)
        if date["rate"] != date1["rate"]:
            print('Курс изменился!')
            print(result)
            send_telegram_message(result)
            data = {"currency": currency, "rate": rate, "timestamp": timestamp}
            save_to_json(data)
        else:
            print('Курс не изменился')

        for i in range(1, 5):
            print_time()
            time.sleep(60)

        # choice = '2'
        # if choice == "1":
        #     continue
        # elif choice == "2":
        #     break
        # else:
        #     print("Некорректный ввод")


def send_telegram_message(my_text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': my_text
    }
    responce = requests.post(url, json=payload)
    return responce


def get_currency_rate(currency: str) -> float:
    """Получает курс валюты и возвращает его в виде float"""
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    response_data = response.json()
    rate = response_data['Valute'][currency]['Value']
    # rate = 99.444
    return rate


def save_to_json(data: dict) -> None:
    with open(CURRENCY_RATES_FILE, "a") as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data, json_file)


def load_from_json(file_name) -> dict:
    with open(file_name, encoding='utf-8') as file:
        content = file.read()
        file_data = json.loads(content)
    return file_data


def print_time():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Время:", current_time)


if __name__ == '__main__':
    main()
