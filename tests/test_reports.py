import json
import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reports import save_report, spending_by_category


class TestSpendingByCategory:
    """Тесты для функции spending_by_category"""

    def test_spending_by_category_exists(self):
        """Тест что функция существует"""
        assert callable(spending_by_category)

    def test_spending_by_category_returns_dataframe(self):
        """Тест что функция возвращает DataFrame"""
        # Создаем тестовые данные
        test_data = pd.DataFrame(
            {
                "category": ["food", "transport", "food", "entertainment"],
                "amount": [100, 50, 200, 150],
                "date": ["2024-01-15", "2024-01-20", "2024-02-10", "2024-02-15"],
            }
        )

        result = spending_by_category(test_data, "food", "2024-03-01")
        assert isinstance(result, pd.DataFrame)

    def test_spending_by_category_correct_sum(self):
        """Тест правильного подсчета суммы"""
        test_data = pd.DataFrame(
            {
                "category": ["food", "transport", "food", "food"],
                "amount": [100, 50, 200, 300],
                "date": ["2024-01-15", "2024-01-20", "2024-02-10", "2024-02-20"],
            }
        )

        result = spending_by_category(test_data, "food", "2024-03-01")

        # Проверяем что сумма правильная
        assert len(result) == 1
        assert result.iloc[0]["category"] == "food"
        assert result.iloc[0]["amount"] == 600  # 100 + 200 + 300

    def test_spending_by_category_no_data(self):
        """Тест когда нет данных по категории"""
        test_data = pd.DataFrame(
            {
                "category": ["transport", "entertainment"],
                "amount": [50, 150],
                "date": ["2024-01-15", "2024-01-20"],
            }
        )

        result = spending_by_category(test_data, "food", "2024-03-01")

        # Должен вернуть пустой DataFrame с правильными колонками
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "category" in result.columns
        assert "amount" in result.columns

    def test_spending_by_category_without_date(self):
        """Тест без указания даты"""
        test_data = pd.DataFrame(
            {
                "category": ["food", "food"],
                "amount": [100, 200],
                "date": ["2024-01-15", "2024-01-20"],
            }
        )

        # Должен работать без даты
        result = spending_by_category(test_data, "food")
        assert isinstance(result, pd.DataFrame)


class TestSaveReport:
    """Тесты для декоратора save_report"""

    def test_save_report_exists(self):
        """Тест что декоратор существует"""
        assert callable(save_report)

    def test_save_report_without_parameters(self):
        """Тест декоратора без параметров"""

        @save_report
        def test_function():
            return {"test": "data"}

        result = test_function()
        assert result == {"test": "data"}

    def test_save_report_with_filename(self):
        """Тест декоратора с именем файла"""

        @save_report("test_report.json")
        def test_function():
            return pd.DataFrame({"col": [1, 2, 3]})

        result = test_function()
        assert isinstance(result, pd.DataFrame)

    def test_save_report_with_empty_parentheses(self):
        """Тест декоратора с пустыми скобками"""

        @save_report()
        def test_function():
            return [1, 2, 3]

        result = test_function()
        assert result == [1, 2, 3]


if __name__ == "__main__":
    # Тесты для spending_by_category
    test_category = TestSpendingByCategory()
    test_category.test_spending_by_category_exists()
    test_category.test_spending_by_category_returns_dataframe()
    test_category.test_spending_by_category_correct_sum()
    test_category.test_spending_by_category_no_data()
    test_category.test_spending_by_category_without_date()

    # Тесты для save_report
    test_report = TestSaveReport()
    test_report.test_save_report_exists()
    test_report.test_save_report_without_parameters()
    test_report.test_save_report_with_filename()
    test_report.test_save_report_with_empty_parentheses()

    print("✅ Все тесты reports пройдены")
