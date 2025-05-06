from sg_windows import main_window
from utils import export_csv_records, write_finance_data


if __name__ == "__main__":
    HEADERS = ["item", "category", "income", "expense"]
    write_finance_data([], HEADERS)
    export_csv_records()
    main_window(HEADERS)