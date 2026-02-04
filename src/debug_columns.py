import pandas as pd

def check_columns():
    print("--- 1. CENSUS COLUMNS ---")
    try:
        df = pd.read_csv('data/raw/india-districts-census-2011.csv')
        print(df.columns.tolist()[:10]) # Print first 10
    except Exception as e:
        print(e)

    print("\n--- 2. EV SALES COLUMNS ---")
    try:
        df = pd.read_csv('data/raw/EV_Dataset.csv')
        print(df.columns.tolist())
    except Exception as e:
        print(e)

    print("\n--- 3. STATIONS COLUMNS (The one causing error) ---")
    try:
        df = pd.read_csv('data/raw/ev-charging-stations-india.csv')
        print(df.columns.tolist())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_columns()