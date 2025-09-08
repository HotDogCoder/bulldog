import os
import xlrd
import pandas as pd

def read_xls_with_xlrd(file_path, sheet_name="Users"):
    try:
        workbook = xlrd.open_workbook(file_path, ignore_workbook_corruption=True)
        sheet = workbook.sheet_by_name(sheet_name)

        # Header
        header = sheet.row_values(0)

        # Rows
        data = []
        for row in range(1, sheet.nrows):
            values = []
            for val in sheet.row_values(row):
                # Convert all to string to preserve zeros/spaces
                if isinstance(val, float) and val.is_integer():
                    val = str(int(val))
                else:
                    val = str(val)
                values.append(val)
            data.append(values)

        df = pd.DataFrame(data, columns=header)
        return df
    except Exception as e:
        print(f"❌ Could not read {file_path}: {e}")
        return None


def combine_excel_files(input_folder, output_file):
    expected_header = ["ID", "Login", "Name", "Currency", "E-mail", "Phone",
                       "Balance", "Deposit", "Withdraw", "Profit", "Game"]

    all_dataframes = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".xls"):
            file_path = os.path.join(input_folder, filename)
            print(f"Reading {file_path} (Users sheet)...")

            df = read_xls_with_xlrd(file_path, sheet_name="Users")
            if df is None:
                continue

            # Keep only expected columns if present
            if all(col in df.columns for col in expected_header):
                df = df[expected_header]
                all_dataframes.append(df)
            else:
                print(f"⚠️ Skipping {file_path}, missing expected columns")

    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # Export to XLS (old Excel format)
        combined_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"✅ Combined Excel saved to {output_file}")
    else:
        print("❌ No valid Excel files found in the folder.")


if __name__ == "__main__":
    input_folder = "/Users/ditsy/Django/bulldog/downloads/excel_files_zera_2"   # 📂 Cambia esta ruta
    output_file = "combined.xls"           # 📄 Salida en formato XLS
    combine_excel_files(input_folder, output_file)
