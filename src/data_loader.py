import datetime

import pandas as pd

from develop_fun.get_logger import get_logger


def input_date():
    answer = input(
        "Введите готовую дату в формате:%d.%m.%Y %H:%M:%S\nИли по умолчанию будет выбрана дата:\n"
        "15.11.2021 04:57:31\nВвод:"
    )
    default_date = "15.11.2021 04:57:31"

    try:
        input_date = datetime.strptime(answer, "%d.%m.%Y %H:%M:%S")
        print(f"Дата принята:{answer}")
        return input_date

    except Exception as e:
        print(f"Будет использована дата по умолчанию {default_date} ")
        return default_date


def read_excel(path) -> pd.DataFrame:
    """
    Читает excel переводит в pd.DataFrame
    :param path:
    :return: DataFrame
    """
    logger = get_logger()
    try:
        df = pd.read_excel(path)
        logger.info(f"Файл прочитан:\n{df}")
        return df

    except Exception as e:
        logger.error(f"Не получилось прочитать файл, ошибка : {e}")
        return pd.DataFrame


def get_operation_with_range(operation_df: pd.DataFrame, date_end: str) -> pd.DataFrame:
    """
    Фильтрует по дате операции из таблицы
    :param operation_df: pd.DataFrame
    :param date_end:str
    :return: pd.DataFrame
    """
    logger = get_logger()
    first_date = datetime.datetime.strptime(date_end, "%d.%m.%Y %H:%M:%S").strftime(
        "%01.%m.%Y %00:%00:%00"
    )

    logger.info(f"получили дату в формтате 'str'\nДАТА 1 дня месяца:{first_date}")

    df_filter = operation_df[
        (first_date <= operation_df["Дата операции"]) & (operation_df["Дата операции"] <= date_end)
    ]
    logger.info("Операции из таблицы отфильтрованы по дате")
    return df_filter


def get_cards_num_and_sum(operation_df: pd.DataFrame):
    """
    Получить номер карты, кэшбэк и все расходы по ней
    :param operation_df:
    :return:DataFrame
    """
    logger = get_logger()

    # расходы
    operation_df = operation_df[operation_df["Сумма платежа"] < 0]
    logger.info("Оставили только строки расходов в pd.DataFrame")
    operation_df = operation_df[operation_df["Статус"] == "OK"]
    logger.info('оставили только те, в которых статус "ОК" ')
    result = (
        operation_df[["Номер карты", "Сумма платежа", "Кэшбэк"]]
        .groupby("Номер карты")
        .sum()
        .reset_index()
    )
    logger.info(
        "Создали список номер карты, кэшбэк и все расходы по ней\n"
        'в формате: "class pandas.core.frame.DataFrame" '
    )
    return result


def top_5_transactions(df):
    """
    топ 5 платежей
    :param df:
    :return:dict
    """
    top_transaction = df.copy()
    top_transaction["abs_amount"] = top_transaction["Сумма платежа"].abs()
    top_5 = top_transaction.nlargest(5, "abs_amount")
    result = {
        "top_transactions": [
            {
                "date": row["Дата операции"],
                "amount": float(row["Сумма платежа"]),  # ← здесь оригинальная сумма с минусом
                "category": row.get("Категория", ""),
                "description": row.get("Описание", ""),
            }
            for _, row in top_5.iterrows()
        ]
    }

    return result


# operations = read_excel(PATH_TO_OPERATION)
# operations = operations[['Дата операции','Описание', 'Сумма платежа']]
# operations_list = operations.to_dict('records') # список словарей
# operations_json = json.dumps(operations_list, ensure_ascii=False, indent= 4)
# print(operations_json)
# print(type(operations_json))

# res = get_operation_with_range(operation_df=read_excel(PATH_TO_OPERATION) , date_end='23.12.2021 02:34:12' )
# print(type(get_cards_num_and_sum(operation_df=res)))
