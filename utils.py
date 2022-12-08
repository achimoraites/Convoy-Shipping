import re
import pandas as pd


def read_file(file_name, sheet_name):
    if file_name.endswith('.xlsx'):
        df = pd.read_excel(file_name, sheet_name=sheet_name, dtype=str)
        number_of_rows = df.shape[0]
        lines = "line was" if number_of_rows == 1 else "lines were"
        new_file_name = file_name.replace('.xlsx', '.csv')
        print("{} {} imported to {}".format(number_of_rows, lines, new_file_name))
        df.to_csv(new_file_name, index=None, header=True)
        return df
    else:
        return pd.read_csv(file_name, dtype=str)


def clean_up_integers_in_column(df, col):
    invalid_entries = get_invalid_entries(df, col)
    return clean_up_cells(df, invalid_entries, col)


def get_checked_filename(file_name):
    if file_name.endswith('.xlsx'):
        return file_name.replace('.xlsx', '[CHECKED].csv')
    else:
        return file_name.replace('.csv', '[CHECKED].csv')




# HELPERS


def clean_up_cells(df, invalid_items, column_name, regex=r"\d+", cells_fixed=0):
    for index, _ in invalid_items.items():
        # print('item', df[column_name][index])
        digits = re.search(regex, df[column_name][index])
        if digits is not None:
            # print('group', non_digits.group())
            df[column_name][index] = digits.group()
            # print(df[column_name][index])
            cells_fixed += 1
    return cells_fixed


def get_invalid_entries(df, column, regex=r"[a-zA-Z ]"):
    counts = df[column].str.count(regex)
    return counts[counts > 0]
