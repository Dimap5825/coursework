import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import get_greeting


class TestGetGreeting:
    """Простые тесты для get_greeting"""

    def test_greeting_morning(self):
        result = get_greeting("15.11.2021 08:30:00")
        assert result == "Доброе утро"

    def test_greeting_afternoon(self):
        result = get_greeting("15.11.2021 14:30:00")
        assert result == "Добрый день"

    def test_greeting_evening(self):
        result = get_greeting("15.11.2021 20:30:00")
        assert result == "Добрый вечер"

    def test_greeting_night(self):
        result = get_greeting("15.11.2021 02:30:00")
        assert result == "Доброй ночи"

    def test_greeting_invalid_format(self):
        result = get_greeting("invalid-date")
        assert result == "Добрый день"


class TestFunctionsExist:
    """Просто проверяем что функции существуют"""

    def test_get_currency_rates_exists(self):
        from src.utils import get_currency_rates

        assert callable(get_currency_rates)

    def test_get_stock_prices_exists(self):
        from src.utils import get_stock_prices

        assert callable(get_stock_prices)


if __name__ == "__main__":
    test = TestGetGreeting()
    test.test_greeting_morning()
    test.test_greeting_afternoon()
    test.test_greeting_evening()
    test.test_greeting_night()
    print("✅ Все простые тесты пройдены")
