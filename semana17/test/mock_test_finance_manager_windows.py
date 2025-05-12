import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from finance_manager import FinanceManager
from unittest.mock import patch, MagicMock


@pytest.fixture
def mocked_finance_manager_with_window():
    with patch('finance_manager.InterfaceTransactionHandler') as MockHandler, \
         patch('finance_manager.InterfaceStructure') as MockStructure, \
         patch('finance_manager.sg.Window') as MockWindow:

        # Mock the handler
        mock_handler = MockHandler.return_value
        mock_handler.load_finance_data.return_value = (["header1"], [["row1"]])
        mock_handler.load_categories.return_value = ["MockedCategory"]
        mock_handler.run_main_window = MagicMock()

        # Mock the structure layout
        mock_structure = MockStructure.return_value
        mock_structure.main_layout.return_value = [['MockedLayout']]

        # Mock the sg.Window constructor
        mock_window_instance = MagicMock()
        MockWindow.return_value = mock_window_instance

        fm = FinanceManager()
        yield fm, mock_handler, mock_window_instance


def test_main_window_calls_run(mocked_finance_manager_with_window):
    # Arrange
    fm, mock_handler, mock_window = mocked_finance_manager_with_window

    # Act
    fm.main_window()

    # Assert: Make sure the window was created and handler.run_main_window was called
    mock_handler.run_main_window.assert_called_once_with(mock_window, mock_handler, fm, fm.data)

def test_category_window_calls_run(mocked_finance_manager_with_window):
    # Arrange
    fm, mock_handler, mock_window = mocked_finance_manager_with_window

    # Act
    fm.category_window()

    # Assert: Make sure the window was created and handler.run_main_window was called
    mock_handler.run_category_window.assert_called_once_with(mock_window, mock_handler)

def test_income_window_calls_run(mocked_finance_manager_with_window):
    # Arrange
    fm, mock_handler, mock_window = mocked_finance_manager_with_window

    # Act
    fm.income_window()

    # Assert: Make sure the window was created and handler.run_main_window was called
    mock_handler.run_income_window.assert_called_once_with(mock_window, mock_handler, fm.data)

def test_expense_window_calls_run(mocked_finance_manager_with_window):
    # Arrange
    fm, mock_handler, mock_window = mocked_finance_manager_with_window

    # Act
    fm.expense_window()

    # Assert: Make sure the window was created and handler.run_main_window was called
    mock_handler.run_expense_window.assert_called_once_with(mock_window, mock_handler, fm.data)