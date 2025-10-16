import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from config import PATH_TO_USER_SETTINGS
from develop_fun.get_logger import get_logger

logger = get_logger()


def get_greeting(date_time: str) -> str:
    """
    Возвращает приветствие в зависимости от времени
    :param date_time:
    :return: str
    """
    try:
        time_obj = datetime.strptime(date_time, "%d.%m.%Y %H:%M:%S")
        hour = time_obj.hour

        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except Exception as e:
        logger.error(f"Ошибка в get_greeting: {e}")
        return "Добрый день"


def get_currency_rates():
    """
    курс валют из файла с настройками пользователя
    :return: dict
    """

    logger = get_logger()
    try:
        with open(PATH_TO_USER_SETTINGS, "r") as f:
            data_setting = json.load(f)

        currency_list = data_setting["user_currencies"]
        logger.info(f"Список валют пользователя:{currency_list}")
    except Exception as e:
        logger.warning(f"Ошибка при получении курса валют \nОшибка:{e}")

    # for currency in currency_list:

    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url=url)
        response.raise_for_status()
        currency_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API ЦБ РФ: {e}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при разборе JSON: {e}")
        return

    result = {}
    for currency in currency_list:
        if currency in currency_data["Valute"]:
            rate = currency_data["Valute"][currency]["Value"]
            result[currency] = rate
            logger.info(f"{currency}: {rate}")
        else:
            logger.warning(f"Валюта {currency} не найдена в API")
    return result


def get_stock_prices():
    """
    Получение цен акций по ApI и тикером из user_settings.json
    :return:dict
    """
    load_dotenv()
    logger = get_logger()
    result = {}
    try:
        with open(PATH_TO_USER_SETTINGS, "r") as f:
            data_setting = json.load(f)

        tickers_list = data_setting["user_stocks"]
        logger.info(f"Список тикеров пользователя:{tickers_list}")
    except Exception as e:
        logger.warning(f"Ошибка при получении списков тикеров из настроек  \nОшибка:{e}")

    # ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    # logger.info(f'получили api ключ {ALPHA_VANTAGE_API_KEY}')
    API_KEY_FINHUB = os.getenv("API_KEY_FINHUB")
    logger.info(f"Получили ключ {API_KEY_FINHUB}")
    action_list = []
    for ticker in tickers_list:
        # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
        url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={API_KEY_FINHUB}"
        response = requests.get(url=url)
        logger.info(f"API вернул {response} для тикера:{ticker}")
        response.raise_for_status()

        data = response.json()
        logger.info(f"API вернул :{data}")

        action_list.append({ticker: data["c"]})

    result["stock_prices"] = action_list
    return result


# print(get_stock_prices())
