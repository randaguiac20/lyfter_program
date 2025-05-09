from interface_manager import InterfaceTransactionHandler, InterfaceStructure
import FreeSimpleGUI as sg



class FinanceManager:
    def __init__(self):
        self.income_expense = False
        self.int_transaction_handler = InterfaceTransactionHandler()
        self.headers, self.data = self.int_transaction_handler.load_finance_data()
        
    def income_window(self):
        handler = self.int_transaction_handler
        layout = InterfaceStructure(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Incomes', layout.income_layout, resizable=True)
        # Event Loop to process
        handler.run_income_window(window, handler, self.data)

    def expense_window(self):
        handler = self.int_transaction_handler
        layout = InterfaceStructure(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Expense', layout.expense_layout, resizable=True)
        # Event Loop to process
        handler.run_expense_window(window, handler, self.data)

    def category_window(self):
        handler = self.int_transaction_handler
        layout = InterfaceStructure(self.data, self.headers, handler)
        window = sg.Window("Create a new category!", layout.category_layout)
        # Event loop
        handler.run_category_window(window, handler)

    def main_window(self):
        sg.theme('DarkBlue')
        handler = self.int_transaction_handler
        layout = InterfaceStructure(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Finances', layout.main_layout, resizable=True)
        # Event Loop to process
        categories = handler.load_categories()
        handler.run_main_window(window, handler,
                                self, self.data)
