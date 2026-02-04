import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

def clean_and_merge():
    print("Loading raw datasets...")
    
    # 1. Load Census Data
    census = pd.read_csv('data/raw/india-districts-census-2011.csv')
    
    # 2. Load EV Sales Data
    ev_sales = pd.read_csv('data/raw/EV_Dataset.csv')
    
    # 3. Load Charging Stations
    stations = pd.read_csv('data/raw/ev-charging-stations-india.csv')

    print(f"Raw Dimensions -> Census: {census.shape}, EV Sales: {ev_sales.shape}, Stations: {stations.shape}")

    # --- STEP 1: STANDARDIZE COLUMN NAMES ---
    # Fix the error: Rename specific columns to 'State' so they match
    print("Standardizing column names...")
    
    # Census: 'State name' -> 'State'
    census.rename(columns={'State name': 'State', 'District name': 'District'}, inplace=True)
    
    # Stations: 'state' -> 'State' (This was the bug)
    stations.rename(columns={'state': 'State'}, inplace=True)
    
    # EV Sales already has 'State', so we are good there.

    # --- STEP 2: STANDARDIZE TEXT (Title Case) ---
    # Ensure "Delhi" matches "delhi" by making everything Title Case
    census['State'] = census['State'].str.title()
    ev_sales['State'] = ev_sales['State'].str.title()
    stations['State'] = stations['State'].str.title()

    # --- STEP 3: AGGREGATE CHARGING STATIONS ---
    # Count stations per state
    station_counts = stations.groupby('State').size().reset_index(name='Station_Count')
    
    # --- STEP 4: AGGREGATE EV SALES ---
    # The EV dataset has multiple rows per state (broken by year/vehicle type)
    # We need to sum them up to get "Total EV Sales per State"
    # Column is 'EV_Sales_Quantity' based on your debug output
    ev_sales_agg = ev_sales.groupby('State')['EV_Sales_Quantity'].sum().reset_index()
    ev_sales_agg.rename(columns={'EV_Sales_Quantity': 'Total_EV_Sales'}, inplace=True)

    # --- STEP 5: MERGE DATASETS ---
    print("Merging datasets...")
    
    # Merge 1: Census + EV Sales
    merged_df = pd.merge(census, ev_sales_agg, on='State', how='left')
    
    # Merge 2: + Charging Stations
    merged_df = pd.merge(merged_df, station_counts, on='State', how='left')
    
    # Fill NaN (States with no recorded EV sales or stations get 0)
    merged_df['Total_EV_Sales'] = merged_df['Total_EV_Sales'].fillna(0)
    merged_df['Station_Count'] = merged_df['Station_Count'].fillna(0)

    # --- STEP 6: FEATURE SELECTION ---
    # Select columns for Clustering
    # We use: Population, Literacy (derived), EV Sales, Station Count
    
    # Census column is 'Literate', convert to Rate if needed or use raw
    feature_cols = ['Population', 'Literate', 'Total_EV_Sales', 'Station_Count']
    
    # Drop rows with missing Census data (should be rare)
    merged_df = merged_df.dropna(subset=['Population', 'Literate'])
    
    # --- STEP 7: SCALING ---
    print("Normalizing data for PCA...")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(merged_df[feature_cols])
    
    # Create final clean DataFrame
    df_processed = pd.DataFrame(scaled_data, columns=feature_cols)
    
    # Attach Metadata back
    df_processed.insert(0, 'State', merged_df['State'])
    df_processed.insert(1, 'District', merged_df['District'])
    
    output_path = 'data/processed/ev_market_final.csv'
    df_processed.to_csv(output_path, index=False)
    
    print(f"\n[Success] Preprocessing Complete!")
    print(f"Final Dataset: {df_processed.shape} rows")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    clean_and_merge()