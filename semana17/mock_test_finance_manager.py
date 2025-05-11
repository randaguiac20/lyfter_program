import pytest
from finance_manager import FinanceManager
from unittest.mock import MagicMock, patch


@pytest.fixture
def mocked_finance_manager_return_value():
    with patch('finance_manager.InterfaceTransactionHandler') as MockHandler:

        # Mock load_finance_data return
        mock_handler_instance = MockHandler.return_value
        mock_handler_instance.load_finance_data.return_value = (["header1", "header2"], [["row1", "row2"]])
        mock_handler_instance.load_categories.return_value = ["Category1", "Category2"]

        yield FinanceManager()

@pytest.fixture
def mocked_finance_manager_validate_attributes():
    with patch('finance_manager.InterfaceStructure') as MockStructure:

        # Mock layout with layout attributes
        mock_structure_instance = MockStructure.return_value
        mock_structure_instance.income_layout = [['Income Layout']]
        mock_structure_instance.expense_layout = [['Expense Layout']]
        mock_structure_instance.category_layout = [['Category Layout']]
        mock_structure_instance.main_layout = [['Main Layout']]

        yield FinanceManager()
