import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_insights():
    print("Loading Data for Insights...")
    
    # 1. Load the CLUSTERS (Has Cluster_ID + State/District)
    try:
        df_clusters = pd.read_csv('outputs/ev_market_clusters.csv')
    except FileNotFoundError:
        raise FileNotFoundError("Could not find 'outputs/ev_market_clusters.csv'. Run Phase 4 first.")

    # 2. Load the ORIGINAL FEATURES (Has Population, Literacy, EV Sales)
    # We need this because the cluster file only has "PC1", "PC2", etc.
    try:
        df_original = pd.read_csv('data/processed/ev_market_final.csv')
    except FileNotFoundError:
        raise FileNotFoundError("Could not find 'data/processed/ev_market_final.csv'. Run Phase 2 first.")

    # 3. MERGE THEM
    # We merge on State & District to get a Master Dataset: [Dist, State, Features..., Cluster_ID]
    print("Merging Cluster IDs with Original Socio-Economic Data...")
    df = pd.merge(df_original, df_clusters[['State', 'District', 'Cluster_ID']], on=['State', 'District'])

    # --- STEP 1: CLUSTER PROFILING ---
    print("\n--- CLUSTER PROFILES (Averages) ---")
    
    # Calculate average stats per cluster
    # numeric_only=True ensures we don't try to average text columns
    profile = df.groupby('Cluster_ID').mean(numeric_only=True)
    
    # Add a count of districts in each cluster
    profile['District_Count'] = df['Cluster_ID'].value_counts().sort_index()
    
    # Display the metrics we care about
    # Check if columns exist before printing (to avoid errors)
    cols_to_show = ['Population', 'Literate', 'Total_EV_Sales', 'Station_Count', 'District_Count']
    available_cols = [c for c in cols_to_show if c in profile.columns]
    
    print(profile[available_cols])

    # --- STEP 2: IDENTIFYING THE "UNTAPPED" SEGMENT ---
    # Logic: Find the cluster with High Literacy but Low EV Sales
    
    # Sort by Literacy (High to Low)
    sorted_clusters = profile.sort_values(by='Literate', ascending=False)
    
    # Best performing cluster (Likely Metro/Tier-1)
    leader_id = sorted_clusters.index[0]
    
    # The "Opportunity" is usually the next best cluster (Tier-2)
    # It has good literacy but sales are not yet saturated
    opportunity_id = sorted_clusters.index[1] 
    
    opportunity_districts = profile.loc[opportunity_id, 'District_Count']
    total_districts = len(df)
    opportunity_pct = (opportunity_districts / total_districts) * 100
    
    insight_text = (
        f"Strategic Insight:\n"
        f"Cluster {opportunity_id} is the 'High-Growth Opportunity'.\n"
        f" - It has high Literacy ({profile.loc[opportunity_id, 'Literate']:.2f} avg) indicating awareness,\n"
        f" - But significantly lower EV Sales than the Leader (Cluster {leader_id}).\n"
        f" - This segment covers {opportunity_pct:.1f}% of India ({int(opportunity_districts)} districts)."
    )
    print("\n" + insight_text)

    # --- STEP 3: VISUALIZATION ---
    print("Generating Insight Charts...")
    
    # Normalize data for the chart (0-1 scale) so big numbers don't hide small numbers
    plot_data = profile[available_cols[:-1]].copy() # Exclude District_Count for plotting
    for col in plot_data.columns:
        plot_data[col] = plot_data[col] / plot_data[col].max()
    
    plot_data = plot_data.reset_index()
    plot_data_melted = plot_data.melt(id_vars='Cluster_ID', var_name='Metric', value_name='Relative_Score')

    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_data_melted, x='Cluster_ID', y='Relative_Score', hue='Metric', palette='viridis')
    
    plt.title('Market Segmentation Profile (Normalized Scores)')
    plt.ylabel('Relative Strength (0 to 1)')
    plt.xlabel('Consumer Persona (Cluster)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    chart_path = 'outputs/figures/market_opportunity_chart.png'
    plt.savefig(chart_path)
    print(f"Chart saved to: {chart_path}")

    # --- STEP 4: SAVE REPORT ---
    report_path = 'outputs/reports/final_strategy.txt'
    with open(report_path, 'w') as f:
        f.write("=== EV-STRAT: MARKET INTELLIGENCE REPORT ===\n\n")
        f.write("1. SEGMENTATION SUMMARY\n")
        f.write(profile[available_cols].to_string())
        f.write("\n\n2. STRATEGIC RECOMMENDATION\n")
        f.write(insight_text)
        f.write("\n\n3. ACTION PLAN\n")
        f.write(f"   - Target Marketing: Focus on Cluster {opportunity_id} (High Literacy/Low Sales).\n")
        f.write(f"   - Infrastructure: Prioritize Charging Stations in Cluster {leader_id} to support existing volume.\n")
    
    print(f"Full Strategy Report saved to: {report_path}")

if __name__ == "__main__":
    generate_insights()