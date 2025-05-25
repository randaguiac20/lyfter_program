from interface_manager import (InterfaceTransactionHandler,
                               InterfaceStructure, Category)
import FreeSimpleGUI as sg



class FinanceManager:
    def __init__(self):
        self.income_expense = False
        self.int_transaction_handler = InterfaceTransactionHandler()
        self.category = Category()
        self.structure = InterfaceStructure()
        self.headers, self.data = self.int_transaction_handler.load_finance_data()
        self.categories = self.category.load_categories()
        
    def income_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.income_layout(self.data, self.headers, self.category)
        # Create the Window
        window = sg.Window('My Incomes', layout, resizable=True)
        # Event Loop to process
        handler.run_income_window(window, handler, self.data, self.category)

    def expense_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.expense_layout(self.data, self.headers, self.category)
        # Create the Window
        window = sg.Window('My Expense', layout, resizable=True)
        # Event Loop to process
        handler.run_expense_window(window, handler, self.data, self.category)

    def category_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.category_layout()
        window = sg.Window("Create a new category!", layout)
        # Event loop
        handler.run_category_window(window, self.category)

    def main_window(self):
        sg.theme('DarkBlue')
        handler = self.int_transaction_handler
        layout = self.structure.main_layout(self.data, self.headers)
        # Create the Window
        window = sg.Window('My Finances', layout, resizable=True)
        # Event Loop to process
        self.category.load_categories()
        handler.run_main_window(window, self, self.data)
