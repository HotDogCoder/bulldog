import os
import pandas as pd

def read_file(file_path, header):
    # Try Excel first
    try:
        return pd.read_excel(file_path, engine="xlrd")
    except Exception:
        pass

    # Try CSV
    try:
        return pd.read_csv(file_path, sep=None, engine="python")
    except Exception:
        pass

    # Try HTML (some .xls are actually HTML tables)
    try:
        dfs = pd.read_html(file_path)
        if dfs:
            return dfs[0]  # first table
    except Exception:
        pass

    return None


def combine_files(input_folder, output_file):
    header = ["ID", "Login", "Name", "Currency", "E-mail", "Phone",
              "Balance", "Deposit", "Withdraw", "Profit", "Game"]

    all_dataframes = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            file_path = os.path.join(input_folder, filename)
            print(f"Reading {file_path}...")

            df = read_file(file_path, header)
            if df is None:
                print(f"❌ Could not read {file_path} in any format.")
                continue

            # Ensure correct columns
            missing = [col for col in header if col not in df.columns]
            if missing:
                print(f"⚠️ Skipping {file_path}, missing columns: {missing}")
                continue

            df = df[header]
            all_dataframes.append(df)

    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"✅ Combined CSV saved to {output_file}")
    else:
        print("❌ No valid files found.")

if __name__ == "__main__":
    input_folder = "/Users/ditsy/Django/bulldog/downloads/excel_files_zera_2"  # change this
    output_file = "combined.csv"
    combine_files(input_folder, output_file)
