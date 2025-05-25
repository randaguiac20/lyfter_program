import FreeSimpleGUI as sg
from data_manager import Transaction


class Category:
    def __init__(self):
        self.transaction = Transaction()
        self.write_data = self.transaction.write_csv_file()

    def add_category(self, category):
        print(f"add_category {category}")
        self.transaction.write_txt_file(value=category)

    def load_categories(self):
        categories = self.transaction.read_txt_file()
        return categories

class InterfaceStructure:
    def income_layout(self, data, headers, categories):
        return [
            [sg.Text("Item"), sg.Input(key='-ITEM-', size=(20, 1))],
            [sg.Text("Category"), sg.Combo(categories.load_categories(), key='-CATEGORY-', size=(20, 1))],
            [sg.Text("Income"), sg.Input(default_text=0, key='-INCOME-', size=(20, 1))],
            [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                    auto_size_columns=True, justification='left')],
            [sg.Button("Save"), sg.Button("Exit")]
        ]

    def expense_layout(self, data, headers, categories):
        return [
            [sg.Text("Item"), sg.Input(key='-ITEM-', size=(20, 1))],
            [sg.Text("Category"), sg.Combo(categories.load_categories(), key='-CATEGORY-', size=(20, 1))],
            [sg.Text("Expense"), sg.Input(default_text=0, key='-EXPENSE-', size=(20, 1))],
            [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                    auto_size_columns=True, justification='left')],
            [sg.Button("Save"), sg.Button("Exit")]
        ]

    def category_layout(self):
        return [
            [sg.Text("Enter a new category: ")],
            [sg.Input(key='-NEWCAT-')],
            [sg.Button("Create new category"), sg.Button("Exit")]
        ]

    def main_layout(self, data, headers):
        return [
            [sg.Button("Add New Income"), sg.Button("Add New Expense"), sg.Button("Add New Category")],
            [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                    auto_size_columns=True, justification='left')],
            [sg.Button("Exit")]
        ]


class InterfaceTransactionHandler:
    def __init__(self):
        self.transaction = Transaction()
        self.write_data = self.transaction.write_csv_file()
    
    def load_finance_data(self):
        data = self.transaction.read_csv_file()
        if len(data) == 0:
            data.append([])
        return data[0], data[1:]
    
    def add_income(self, window, values, data):
        item = values['-ITEM-'].strip()
        category = values['-CATEGORY-'].strip()
        income = int(values['-INCOME-'].strip() or 0)
        expense = int(values['-EXPENSE-'].strip() or 0)
        
        if item and category:
            new_row = [item, category, income, expense]
            data.append(new_row)
            self.transaction.write_csv_file(dataset=[new_row])

            # Refresh table view
            data_table = [row for row in data if len(row) == 4]
            window['-TABLE-'].update(values=data_table)
            # Clear inputs
            window['-ITEM-'].update('')
            window['-INCOME-'].update('')
            window['-CATEGORY-'].update('')
        else:
            sg.popup("Please fill in at least Item and Category.")

    def add_expense(self, window, values, data):
        item = values['-ITEM-'].strip()
        category = values['-CATEGORY-'].strip()
        income = int(values['-INCOME-'].strip() or 0)
        expense = int(values['-EXPENSE-'].strip() or 0)
        
        if item and category:
            new_row = [item, category, income, expense]
            data.append(new_row)
            self.transaction.write_csv_file(dataset=[new_row])

            # Refresh table view
            data_table = [row for row in data if len(row) == 4]
            window['-TABLE-'].update(values=data_table)
            # Clear inputs
            window['-ITEM-'].update('')
            window['-EXPENSE-'].update('')
            window['-CATEGORY-'].update('')
        else:
            sg.popup("Please fill in at least Item and Category.")

    def run_income_window(self, window, handler, data, category):
        categories = category.load_categories()
        while True:
            if len(categories[0]) == 0:
                sg.popup("No categories available, add a new category!!")
                event, values = window.read(timeout=1000)
                category.add_category(categories)
                window['-CATEGORY-'].update(values=categories)
            event, values = window.read()
            is_true = self.transaction.check_is_positve_number(values['-INCOME-'].strip())
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            if not is_true:
                sg.popup("Please enter a valid number!!")
            if event == "Save":
                if is_true:
                    values.update({"-EXPENSE-": "0"})
                    handler.add_income(window, values, data)
        window.close()

    def run_expense_window(self, window, handler, data, category):
        categories = category.load_categories()
        while True:
            if len(categories[0]) == 0:
                sg.popup("No categories available, add a new category!!")
                event, values = window.read(timeout=1000)
                category.add_category(categories)
                window['-CATEGORY-'].update(values=categories)
            event, values = window.read()
            is_true = self.transaction.check_is_positve_number(values['-EXPENSE-'].strip())
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            if not is_true:
                sg.popup("Please enter a valid number!!")
            if event == "Save":
                if is_true:
                    values.update({"-INCOME-": "0"})
                    handler.add_expense(window, values, data)
        window.close()

    def run_category_window(self, window, category):
        new_category = None
        while True:
            event, values = window.read(timeout=1000)
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            if event == "Create new category":
                new_category = values['-NEWCAT-'].strip()
                categories = category.load_categories()
                if new_category and new_category not in categories:
                    category.add_category(new_category)
                break
        window.close()

    def run_main_window(self, window, cls, data):
        while True:
            categories = cls.category.load_categories()
            if len(categories[0]) == 0:
                sg.popup("No categories available, add a new category!!")
                event, values = window.read(timeout=1000)
                cls.category_window()
            event, values = window.read(timeout=1000)
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            if event == "Add New Category":
                cls.category_window()
            if event == "Add New Income":
                cls.income_window()
            if event == "Add New Expense":
                cls.expense_window()
            # Refresh table view
            data_table = [row for row in data if len(row) == 4]
            window['-TABLE-'].update(values=data_table)
        window.close()
        self.transaction.export_csv_file()
