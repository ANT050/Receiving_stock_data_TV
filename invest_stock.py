import requests
import json


def get_market_url():
    while True:
        try:
            market = int(input('\nВыберите рынок: 1 - Русский рынок, 2 - Американский рынок: '))
            if market == 1:
                return 'https://scanner.tradingview.com/russia/scan'
            elif market == 2:
                return 'https://scanner.tradingview.com/america/scan'
            else:
                print('Пожалуйста, выберите 1 или 2.')
        except ValueError:
            print('Пожалуйста, введите число.')


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/118.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/plain, */*; q=0.01',
        'Content-Type': 'application/json; charset=utf-8'

    }

    request_body = {
        'options': {'lang': 'ru'},
        'columns': [
            'name', 'description', 'close', 'change_abs', 'change', 'sector', 'currency', 'exchange'
        ]
    }

    json_request_body = json.dumps(request_body)
    response = requests.post(url, headers=headers, data=json_request_body)
    return response.json()


def search_stock_by_name_or_ticker(data, search_term):
    results = []
    for entry in data['data']:
        d_param = entry['d']
        name = d_param[1]
        ticker = d_param[0]

        if search_term.lower() in name.lower() or search_term.lower() == ticker.lower():
            results.append(d_param)

    return results


def process_data(data):
    search_term = input("Введите название акции или тикер: ")
    stock_data_list = search_stock_by_name_or_ticker(data, search_term)

    if stock_data_list:
        for stock_data in stock_data_list:
            output = f'\nФинансовый инструмент: {stock_data[1]}\n' \
                     f'Тикер: {stock_data[0]}\n' \
                     f'Текущая цена: {stock_data[2]} {stock_data[6]}\n' \
                     f'Изменение цены: {stock_data[3]} {stock_data[6]}\n' \
                     f'Процент изменения цены: {stock_data[4]} %\n' \
                     f'Биржа: {stock_data[7]}\n'
            print(output)
    else:
        print("Данный финансовый инструмент отсутствует.")


def main():
    market_url = get_market_url()
    data = get_data(market_url)
    process_data(data)


if __name__ == "__main__":
    main()
