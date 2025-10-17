import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import default_search


class TestDefaultSearch:
    """Тесты для функции default_search"""

    def test_default_search_exists(self):
        """Тест что функция существует"""
        assert callable(default_search)

    def test_default_search_empty_string(self):
        """Тест с пустой строкой поиска"""
        result = default_search("")
        assert result == "[]"  # Должен вернуть пустой JSON массив

    def test_default_search_whitespace_string(self):
        """Тест с строкой из пробелов"""
        result = default_search("   ")
        assert result == "[]"  # Должен вернуть пустой JSON массив

    def test_default_search_returns_string(self):
        """Тест что функция возвращает строку (JSON)"""
        result = default_search("test")
        assert isinstance(result, str)

    def test_default_search_valid_json(self):
        """Тест что возвращается валидный JSON"""
        result = default_search("test")
        # Пытаемся распарсить JSON - если не получится, будет ошибка
        parsed = json.loads(result)
        assert isinstance(parsed, list)


if __name__ == "__main__":
    test = TestDefaultSearch()
    test.test_default_search_exists()
    test.test_default_search_empty_string()
    test.test_default_search_whitespace_string()
    test.test_default_search_returns_string()
    test.test_default_search_valid_json()
    print("✅ Все простые тесты services пройдены")
