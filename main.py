import json

from config import PATH_TO_OPERATION
from data_loader import (
    get_cards_num_and_sum,
    get_operation_with_range,
    input_date,
    read_excel,
    top_5_transactions,
)
from utils import get_currency_rates, get_greeting, get_stock_prices


def major(data: str) -> str:
    """
    Реализован набор функций и главную функцию, принимающую на вход строку с датой и временем в формате

    "%d.%m.%Y %H:%M:%S" и возвращающую JSON-ответ со следующими данными:
    Приветствие в формате, где
    — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    По каждой карте:
        последние 4 цифры карты;
        общая сумма расходов;
        кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500.

    :param data:
    :return:
    """
    result = {
        "greeting": get_greeting(date_time=data),
        "cards": get_cards_num_and_sum(
            get_operation_with_range(operation_df=read_excel(PATH_TO_OPERATION), date_end=data)
        ),
        "top_transactions": top_5_transactions(
            df=get_operation_with_range(read_excel(PATH_TO_OPERATION), date_end=data)
        ),
        "currency_rates": get_currency_rates(),  # Курс валют.
        "stock_prices": get_stock_prices(),  # Стоимость акций из S&P500.
    }
    result["cards"] = result["cards"].to_dict(orient="records")

    return json.dumps(result, ensure_ascii=False, indent=2)


# date = '15.11.2021 04:57:31' #для примера
date = input_date()
if __name__ == "__main__":
    # print(type(major(data=date)))
    print(major(date))
    # print(get_greeting(date_time=date))
