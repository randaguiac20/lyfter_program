import pytest
from finance_manager import FinanceManager
from unittest.mock import MagicMock, patch



@pytest.fixture
def test_finance_manager_return_init_values():
    with patch('finance_manager.InterfaceTransactionHandler') as MockHandler:

        # Mock load_categories return
        mock_handler_instance = MockHandler.return_value
        mock_handler_instance.load_finance_data.return_value = (["header1", "header2"], [["row1", "row2"]])
        mock_handler_instance.load_categories.return_value = ["Category1", "Category2"]
        
        yield FinanceManager()

@pytest.fixture
def test_finance_manager_validate_layout_methods():
    with patch('finance_manager.InterfaceStructure') as MockStructure:
        # Mock InterfaceStructure instance
        mock_structure_instance = MagicMock()
        mock_structure_instance = MockStructure.return_value

        # Create a mock return value for income_layout
        mock_structure_instance.income_layout.return_value = [['Mocked Income Layout']]
        mock_structure_instance.expense_layout.return_value = [['Mocked Expense Layout']]
        mock_structure_instance.category_layout.return_value = [['Mocked Category Layout']]
        mock_structure_instance.main_layout.return_value = [['Mocked Main Window Layout']]

        yield FinanceManager()

## Unit Tests
def test_finance_manager_headers_are_correct():
    # Arrange
    headers = ["item","category","income","expense"]
    # Act
    result = FinanceManager().headers
    # Assert
    assert result == headers

def test_finance_manager_initialization_attribute_int_transaction_handler():
    # Arrange
    fm = FinanceManager()
    attribute = True
    # Act
    result = hasattr(fm, 'int_transaction_handler')
    # Assert
    assert result == attribute

def test_finance_manager_initialization_attribute_strcuture():
    # Arrange
    fm = FinanceManager()
    attribute = True
    # Act
    result = hasattr(fm, 'structure')
    # Assert
    assert result == attribute

def test_data_headers_return_values(test_finance_manager_return_init_values):
    fm = test_finance_manager_return_init_values
    assert fm.headers == ["header1", "header2"]

def test_finance_manager_validate_categories(test_finance_manager_return_init_values):
    fm = test_finance_manager_return_init_values
    assert fm.categories == ["Category1", "Category2"]

def test_finance_income_layout(test_finance_manager_validate_layout_methods):
    # Create fake inputs
    fake_data = [['Sales', 'Revenue', '1000']]
    fake_headers = ['Item', 'Category', 'Amount']
    fake_categories = ['Revenue', 'Bonus']

    # Call the mocked income_layout method
    income_layout = test_finance_manager_validate_layout_methods.structure.income_layout(
        fake_data, fake_headers, fake_categories
    )
    assert income_layout == [['Mocked Income Layout']]

def test_finance_expense_layout(test_finance_manager_validate_layout_methods):
    # Create fake inputs
    fake_data = [['Sales', 'Revenue', '1000']]
    fake_headers = ['Item', 'Category', 'Amount']
    fake_categories = ['Revenue', 'Bonus']

    # Call the mocked expense_layout method
    expense_layout = test_finance_manager_validate_layout_methods.structure.expense_layout(
        fake_data, fake_headers, fake_categories
    )
    assert expense_layout == [['Mocked Expense Layout']]

def test_finance_category_layout(test_finance_manager_validate_layout_methods):
    # Create fake inputs
    fake_data = [['Sales', 'Revenue', '1000']]
    fake_headers = ['Item', 'Category', 'Amount']
    fake_categories = ['Revenue', 'Bonus']

    # Call the mocked category_layout method
    category_layout = test_finance_manager_validate_layout_methods.structure.category_layout(
        fake_data, fake_headers, fake_categories
    )
    assert category_layout == [['Mocked Category Layout']]

def test_finance_main_layout(test_finance_manager_validate_layout_methods):
    # Create fake inputs
    fake_data = [['Sales', 'Revenue', '1000']]
    fake_headers = ['Item', 'Category', 'Amount']
    fake_categories = ['Revenue', 'Bonus']

    # Call the mocked main_layout method
    main_layout = test_finance_manager_validate_layout_methods.structure.main_layout(
        fake_data, fake_headers, fake_categories
    )
    assert main_layout == [['Mocked Main Window Layout']]
