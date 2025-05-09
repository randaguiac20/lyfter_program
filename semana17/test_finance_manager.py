import pytest
from finance_manager import FinanceManager

def test_finance_manager_headers_are_correct():
    # Arrange
    headers = ["item","category","income","expense"]
    # Act
    result = FinanceManager().headers
    # Assert
    assert result == headers

