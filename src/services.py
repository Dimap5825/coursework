import json

import pandas as pd

from config import PATH_TO_OPERATION
from develop_fun.get_logger import get_logger


def default_search(found_string:str)-> str:
    """
    Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории.
    :param found_string:
    :return:json str
    """
    logger = get_logger()
    result = []
    found = found_string.lower().strip()
    if not found:
        logger.info('Пустой поисковый запрос')
        return json.dumps([])

    try:
        df = pd.read_excel(PATH_TO_OPERATION,engine="openpyxl")
        logger.info('Файл открылся получили DataFrame')
        inf_in_py_format = df.to_dict(orient='records')
        logger.info('Преобразовали DataFrame в Py(dict)')
    except Exception as e:
        logger.warning(f'Не получилось файл открыть {e}')
        return json.dumps(result)

    for  row in inf_in_py_format:
        try:
            if any(found in str(value).lower() for value in row.values()):
                result.append(row)
        except Exception as e:
            logger.error(f'При поиске {found_string} в строке {row} Ошибка:{e}')
    if result:
        print(f'Найдено {len(result)} совпадений')
        return json.dumps(result,ensure_ascii=False,indent=2)
    else:
        print('Совпадений не найдено')
        return json.dumps(result)
