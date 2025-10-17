from pathlib import Path

PATH = Path(__file__).parent  # корень
PATH_TO_OPERATION = PATH / "data" / "operations.xlsx"  # табличка
PATH_TO_USER_SETTINGS = PATH / "user_settings.json"  # файл с настройками пользователя
PATH_TO_LOG = PATH / "log"  # папка с логами
# https://www.cbr-xml-daily.ru/daily_json.js  # курс валют
# https://www.alphavantage.co/query? # получаем последнюю стоимость акции
PATH_FOR_REPORT = "reports.json"
