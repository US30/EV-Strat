import os
from dotenv import load_dotenv

# 1. Load Credentials BEFORE importing Kaggle
load_dotenv()

# Validate keys
if not os.getenv("KAGGLE_USERNAME") or not os.getenv("KAGGLE_KEY"):
    raise ValueError(
        "Error: Kaggle credentials not found in .env file.\n"
        "Please ensure you have run 'setup_security.py' and pasted your keys into .env"
    )

from kaggle.api.kaggle_api_extended import KaggleApi

def download_real_data():
    print("Authenticating with Kaggle...")
    api = KaggleApi()
    api.authenticate()

    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)

    print(f"Downloading datasets to '{raw_dir}'...")

    # --- Dataset 1: EV Sales Data (UPDATED SOURCE) ---
    # Old source was broken. New source: 'mafzal19/electric-vehicle-sales-by-state-in-india'
    print(" - Downloading: EV Sales by State...")
    try:
        api.dataset_download_files('mafzal19/electric-vehicle-sales-by-state-in-india', path=raw_dir, unzip=True)
    except Exception as e:
        print(f"   [Warning] Could not download EV Sales data: {e}")
        print("   -> Tip: You may need to visit https://www.kaggle.com/datasets/mafzal19/electric-vehicle-sales-by-state-in-india and click 'Agree to Rules'.")

    # --- Dataset 2: Indian Census Data ---
    print(" - Downloading: India Census Data...")
    try:
        api.dataset_download_files('danofer/india-census', path=raw_dir, unzip=True)
    except Exception:
        print("   [Warning] Census data download failed. Check API permissions.")

    # --- Dataset 3: EV Charging Stations ---
    print(" - Downloading: Charging Station Data...")
    try:
        api.dataset_download_files('adityanerlekar31/ev-charging-stations-india', path=raw_dir, unzip=True)
    except Exception:
         print("   [Warning] Charging station data download failed.")

    print("\n[Success] Download process finished.")

def inspect_data():
    print("\nFiles currently in 'data/raw':")
    if os.path.exists("data/raw"):
        for f in os.listdir("data/raw"):
            if not f.startswith('.'):
                print(f" - {f}")
    else:
        print(" - (Directory empty or does not exist)")

if __name__ == "__main__":
    download_real_data()
    inspect_data()