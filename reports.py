import datetime
import json
import pandas as pd
from functools import wraps
from config import PATH_FOR_REPORT
from develop_fun.get_logger import get_logger
from typing import Optional

# Создаём декаратор
def save_report(*args):
    logger = get_logger()
    if len(args) == 1 and callable(args[0]):
        func = args[0]

        @wraps(func)
        def wrapper(*wrapper_args, **wrapper_kwargs):  # ✅
            result = func(*wrapper_args, **wrapper_kwargs)
            data_file = PATH_FOR_REPORT
            if result is not None:
                if isinstance(result, pd.DataFrame):
                    payload = result.to_dict(orient='records')
                    payload = json.dumps(payload, ensure_ascii=False, indent=4)
                elif isinstance(result, (str, list, dict)):
                    payload = json.dumps(result, ensure_ascii=False, indent=4)
                else:
                    print('неизвестный формат данных')
                    logger.error('Неизвестный формат данных')
                    return None
                try:
                    with open(data_file, 'w', encoding='utf-8') as f:
                        f.write(payload)
                        logger.info(f'файл записан в {data_file}')
                except Exception as e:
                    logger.error(f'Ошибка при записи файла:{e}')
                return result
            else:
                logger.error('result пустой')
                return None
        return wrapper

    else:
        file_path= args[0] if args else PATH_FOR_REPORT
        def decorator(func_obj):
            @wraps(func_obj)
            def wrapper_custom(*wrapper_args, **wrapper_kwargs):  # ✅
                result = func(*wrapper_args, **wrapper_kwargs)
                if result is not None:
                    if isinstance(result, pd.DataFrame):
                        payload = result.to_dict(orient = 'records')
                        payload = json.dumps(payload,ensure_ascii=False,indent=4)
                    elif isinstance(result,(str,list,dict)):
                        payload = json.dumps(result,ensure_ascii=False,indent=4)
                    else:
                        print('неизвестный формат данных')
                        logger.error('Неизвестный формат данных')
                        return None
                    try:
                        with open(file_path, 'w',encoding='utf-8') as f:
                            f.write(payload)
                            logger.info(f'файл записан в {file_path}')
                    except Exception as e :
                        logger.error(f'Ошибка при записи файла:{e}')
                    return result
                else:
                    logger.error('result пустой')
                    return None

            return wrapper_custom
        return decorator


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Функция фильтрует транзакции по категории и времени (от переданной даты до трех месяцев назад).
    Если дата не указана, то используется текущая дата. Результат возвращается в виде датафрейма,
    где указаны траты по заданной категории.

    Параметры:
    -----------
    transactions : pd.DataFrame
        Датафрейм с транзакциями. Ожидается, что в нем есть следующие столбцы:
        'category' (категория), 'amount' (сумма), 'date' (дата транзакции в формате 'YYYY-MM-DD').

    category : str
        Название категории, по которой нужно подсчитать траты.

    date : Optional[str], по умолчанию None
        Дата, до которой нужно фильтровать транзакции (в формате 'YYYY-MM-DD').
        Если дата не передана, используется текущая дата.

    Возвращает:
    -----------
    pd.DataFrame
        Датафрейм с одной строкой, содержащей суммарные траты по указанной категории за последние три месяца.
    """
    # Если дата не передана, берём текущую
    if date is None:
        date = datetime.datetime.today().strftime('%Y-%m-%d')

    # Преобразуем строку в объект datetime
    current_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    # Рассчитываем дату 3 месяца назад
    three_months_ago = current_date - datetime.timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    transactions['date'] = pd.to_datetime(transactions['date'])  # Преобразуем в datetime, если нужно
    filtered_transactions = transactions[(transactions['category'] == category) &
                                         (transactions['date'] >= three_months_ago) &
                                         (transactions['date'] <= current_date)]

    # Группируем по категории и суммируем траты
    result = filtered_transactions.groupby('category')['amount'].sum().reset_index()

    return result