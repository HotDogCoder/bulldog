import pandas as pd


class ExcelHelper:

    def __init__(self, path="", sheet_name=None):
        self.path = path
        self.df = pd.read_excel(self.path, engine='openpyxl', sheet_name=sheet_name)

    def get_row(self, sheet, row):
        # print(self.df[sheet].info())
        return self.df[sheet].loc[row]

    def get_row_values(self, row, columns):
        data = [{f'name': columns[i], 'value': row.values[i]} for i in range(len(row.values))]
        return data
