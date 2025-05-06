import FreeSimpleGUI as sg
from utils import (load_finance_data, load_category_data,
                       add_category, write_finance_data,
                       export_csv_records)


def add_income(data, headers):
    categories = load_category_data()

    layout = [
        [sg.Text("Item"), sg.Input(key='-ITEM-', size=(20, 1))],
        [sg.Text("Category"), sg.Combo(categories, key='-CATEGORY-', size=(20, 1))],
        [sg.Text("Income"), sg.Input(key='-INCOME-', size=(20, 1))],
        [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                  auto_size_columns=True, justification='left')],
        [sg.Button("Save"), sg.Button("Exit")]
    ]
    # Create the Window
    window = sg.Window('My Incomes', layout, resizable=True)
    # Event Loop to process
    while True:
        if len(categories[0]) == 0:
            sg.popup("No categories available, add a new category!!")
            event, values = window.read(timeout=1000)
            create_category(categories)
            categories = load_category_data()
            window['-CATEGORY-'].update(values=categories)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Save":
            values.update({"-EXPENSE-": "0"})
            income_expense = True
            add_data(window, values, data,
                     headers, income_expense)
    window.close()

def add_expense(data, headers):
    categories = load_category_data()
    layout = [
        [sg.Text("Item"), sg.Input(key='-ITEM-', size=(20, 1))],
        [sg.Text("Category"), sg.Combo(categories, key='-CATEGORY-', size=(20, 1))],
        [sg.Text("Expense"), sg.Input(key='-EXPENSE-', size=(20, 1))],
        [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                  auto_size_columns=True, justification='left')],
        [sg.Button("Save"), sg.Button("Exit")]
    ]
    
    # Create the Window
    window = sg.Window('My Expense', layout, resizable=True)
    # Event Loop to process
    while True:
        if len(categories[0]) == 0:
            sg.popup("No categories available, add a new category!!")
            event, values = window.read(timeout=1000)
            create_category(categories)
            categories = load_category_data()
            window['-CATEGORY-'].update(values=categories)
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Save":
            values.update({"-INCOME-": "0"})
            income_expense = False
            add_data(window, values, data,
                     headers, income_expense)
    window.close()

def add_data(window, values, data, headers, income_expense):
    item = values['-ITEM-'].strip()
    category = values['-CATEGORY-'].strip()
    income = int(values['-INCOME-'].strip() or 0)
    expense = int(values['-EXPENSE-'].strip() or 0)
    
    if item and category:
        new_row = [item, category, income, expense]
        data.append(new_row)
        write_finance_data([new_row], headers)

        # Refresh table view
        data_table = [row for row in data if len(row) == 4]
        window['-TABLE-'].update(values=data_table)
        # Clear inputs
        if income_expense is True:
            window['-ITEM-'].update('')
            window['-INCOME-'].update('')
            window['-CATEGORY-'].update('')
        if income_expense is False:
            window['-ITEM-'].update('')
            window['-EXPENSE-'].update('')
            window['-CATEGORY-'].update('')
        
        export_csv_records()
    else:
        sg.popup("Please fill in at least Item and Category.")

def create_category(categories):
    layout = [
        [sg.Text("Enter a new category: ")],
        [sg.Input(key='-NEWCAT-')],
        [sg.Button("Create new category"), sg.Button("Exit")]
    ]
    window = sg.Window("Create a new category!", layout)
    new_category = None
    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Create new category":
            new_category = values['-NEWCAT-'].strip()
            if new_category and new_category not in categories:
                add_category(new_category)
            break
    window.close()


def main_window(HEADERS):
    sg.theme('DarkBlue')
    #sg.main_global_pysimplegui_settings()
    headers, data = load_finance_data()
    categories = load_category_data()
    layout = [
        [sg.Button("Add New Income"), sg.Button("Add New Expense"), sg.Button("Add New Category")],
        [sg.Table(values=data, headings=headers, key="-TABLE-", size=(20, 5),
                  auto_size_columns=True, justification='left')],
        [sg.Button("Exit")]
    ]
    # Create the Window
    window = sg.Window('My Finances', layout, resizable=True)
    # Event Loop to process
    while True:
        if len(categories[0]) == 0:
            sg.popup("No categories available, add a new category!!")
            event, values = window.read(timeout=1000)
            create_category(categories)
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Add New Category":
            create_category(categories)
        if event == "Add New Income":
            add_income(data, headers)
        if event == "Add New Expense":
            add_expense(data, headers)
        # Refresh table view
        data_table = [row for row in data if len(row) == 4]
        window['-TABLE-'].update(values=data_table)
    window.close()
