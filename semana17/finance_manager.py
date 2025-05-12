from interface_manager import InterfaceTransactionHandler, InterfaceStructure
import FreeSimpleGUI as sg



class FinanceManager:
    def __init__(self):
        self.income_expense = False
        self.int_transaction_handler = InterfaceTransactionHandler()
        self.structure = InterfaceStructure()
        self.headers, self.data = self.int_transaction_handler.load_finance_data()
        self.categories = self.int_transaction_handler.load_categories()
        
    def income_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.income_layout(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Incomes', layout, resizable=True)
        # Event Loop to process
        handler.run_income_window(window, handler, self.data)

    def expense_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.expense_layout(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Expense', layout, resizable=True)
        # Event Loop to process
        handler.run_expense_window(window, handler, self.data)

    def category_window(self):
        handler = self.int_transaction_handler
        layout = self.structure.category_layout(self.data, self.headers, handler)
        window = sg.Window("Create a new category!", layout)
        # Event loop
        handler.run_category_window(window, handler)

    def main_window(self):
        sg.theme('DarkBlue')
        handler = self.int_transaction_handler
        layout = self.structure.main_layout(self.data, self.headers, handler)
        # Create the Window
        window = sg.Window('My Finances', layout, resizable=True)
        # Event Loop to process
        categories = handler.load_categories()
        handler.run_main_window(window, handler,
                                self, self.data)
