import requests


def get_cbr_zena():
    """Получение курсов валют с сайта Центробанка РФ"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Получаем нужные валюты
        currencies = {
            'USD': data['Valute']['USD'],
            'EUR': data['Valute']['EUR'],
            'GBP': data['Valute']['GBP'],
            'CNY': data['Valute']['CNY']
        }
        # print(currencies)
        # print(data)
        usd = currencies["USD"]["Value"]
        eur = currencies["EUR"]["Value"]
        gbp = currencies["GBP"]["Value"]
        cny = currencies["CNY"]["Value"]
        # print(f"Доллар : {usd}руб ,Евро : {eur}руб,Фунт : {gbp}руб,Юань : {cny}руб")
        dict_zena = {"usd": usd, "eur": eur, "gbp": gbp, "cny": cny}
        return dict_zena

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")

# print(get_cbr_zena()[0])
