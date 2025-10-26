import pytest
import pandas as pd
from unittest.mock import mock_open, patch
from src.reports import spending_by_category, save_report
import datetime

# -------------------- Фикстуры --------------------
@pytest.fixture
def sample_transactions():
    """Возвращает тестовый DataFrame с транзакциями"""
    return pd.DataFrame({
        "category": ["food", "transport", "food", "entertainment"],
        "amount": [100, 50, 200, 150],
        "date": ["2024-01-15", "2024-01-20", "2024-02-10", "2024-02-15"]
    })

@pytest.fixture
def fixed_today():
    """Фиксируем сегодняшнюю дату для тестов без передачи даты"""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 3, 1)
    return FixedDate

# -------------------- Параметризированные тесты spending_by_category --------------------
@pytest.mark.parametrize("category,expected_total", [
    ("food", 300),
    ("transport", 50),
    ("entertainment", 150),
    ("nonexistent", 0),
])
def test_spending_by_category_totals(sample_transactions, category, expected_total):
    """Проверка правильности подсчета total по категории с передачей даты"""
    result = spending_by_category(sample_transactions, category, "2024-03-01")
    assert isinstance(result, dict)
    assert result["category"] == category
    assert result["total"] == expected_total

def test_spending_by_category_without_date(sample_transactions, fixed_today):
    """Проверка работы функции без указания даты с замоком today"""
    with patch("src.reports.datetime.date", fixed_today):
        result = spending_by_category(sample_transactions, "food")
    assert isinstance(result, dict)
    assert result["category"] == "food"
    # Сумма food за последние 3 месяца относительно 2024-03-01
    expected_total = 100 + 200
    assert result["total"] == expected_total

# -------------------- Тестирование save_report --------------------
@pytest.mark.parametrize("return_value", [
    ({"a": 1}),
    (pd.DataFrame({"col": [1, 2, 3]}))
])
def test_save_report_mock(return_value):
    """Тест декоратора save_report с разными типами данных и mock open"""
    m = mock_open()
    with patch("builtins.open", m):
        if isinstance(return_value, pd.DataFrame):
            @save_report("test.json")
            def dummy_func():
                return return_value
        else:
            @save_report
            def dummy_func():
                return return_value

        result = dummy_func()
        # Проверка типа результата
        if isinstance(return_value, pd.DataFrame):
            assert isinstance(result, pd.DataFrame)
        else:
            assert result == return_value
        # Проверяем, что write был вызван
        m.assert_called()
        handle = m()
        handle.write.assert_called()
