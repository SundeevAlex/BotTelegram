import requests, json, datetime, os

CURRENCY_RATES_FILE = "currency_rates.json"
BOT_TOKEN = os.getenv("TELEGRAM_KEY")
CHAT_ID = '6810180613'
API_KEY = os.getenv("APILAYER_KEY")

def main():
    while True:
        # print(BOT_TOKEN)
        # print(API_KEY)
        currency = input("Введите название валюты (USD или EUR): ").upper()
        # currency = 'USD'
        if currency not in ["USD", "EUR"]:
            print("Некорректный ввод")
            break
            # continue
        rate = get_currency_rate(currency)
        # print(rate)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(timestamp)
        result = f"Курс {currency} к рублю: {rate:.2f}"
        print(result)
        send_telegram_message(result)

        data = {"currency": currency, "rate": rate, "timestamp": timestamp}
        save_to_json(data)

        choice = input("Выберите действие: (1 - продолжить, 2 - выйти) ")
        # choice = '2'
        if choice == "1":
            continue
        elif choice == "2":
            break
        else:
            print("Некорректный ввод")


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
    # rate = 97.444
    return rate


def save_to_json(data: dict) -> None:
    with open(CURRENCY_RATES_FILE, "a") as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data_list, json_file)


if __name__ == '__main__':
    main()