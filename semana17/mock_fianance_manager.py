from mock_test_finance_manager import mocked_finance_manager_return_value,mocked_finance_manager_validate_attributes
from finance_manager import FinanceManager


def test_data_headers_return_values(mocked_finance_manager_return_value):
    fm = mocked_finance_manager_return_value
    assert fm.headers == ["header1", "header2"]

def test_mocked_finance_data_categories(mocked_finance_manager_return_value):
    categories = FinanceManager().int_transaction_handler.load_categories()
    assert categories == ["Category1", "Category2"]

def test_mocked_finance_data_categories(mocked_finance_manager_validate_attributes):
    income_layout = FinanceManager().InterfaceStructure().income_layout()
    assert income_layout == ['Income Layout']


if __name__ == "__main__":
    test_data_headers_return_values(mocked_finance_manager_return_value)

