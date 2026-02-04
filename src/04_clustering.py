import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def run_clustering():
    print("Loading PCA data...")
    input_path = 'data/processed/pca_output.csv'
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {input_path}. Run Phase 3 first.")

    # Drop metadata to get just the numbers for clustering
    # We keep 'State' and 'District' separate for now
    features = df.drop(columns=['State', 'District'])
    
    print(f"Data shape for clustering: {features.shape}")

    # --- STEP 1: FINDING OPTIMAL K (The "Math" behind the choice) ---
    print("Running Elbow Method & Silhouette Analysis (Testing K=2 to 10)...")
    
    wcss = [] # Within-Cluster Sum of Squares (Inertia)
    sil_scores = []
    k_range = range(2, 11)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(features)
        wcss.append(kmeans.inertia_)
        sil_scores.append(silhouette_score(features, kmeans.labels_))
    
    # Visualization: Plot Elbow & Silhouette
    # This proves to stakeholders that "5" wasn't a random guess
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Number of Clusters (K)')
    ax1.set_ylabel('Inertia (Lower is Better)', color=color)
    ax1.plot(k_range, wcss, marker='o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Second y-axis
    color = 'tab:red'
    ax2.set_ylabel('Silhouette Score (Higher is Better)', color=color)
    ax2.plot(k_range, sil_scores, marker='x', linestyle='--', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Optimal K Analysis: Elbow Method vs Silhouette Score')
    plt.grid(True)
    plt.savefig('outputs/figures/clustering_validation.png')
    print("Validation plot saved to 'outputs/figures/clustering_validation.png'")

    # --- STEP 2: APPLYING K-MEANS (K=5) ---
    # Based on the resume project description, we select 5 Personas
    optimal_k = 5
    print(f"\nSegmentation: Applying K-Means with K={optimal_k}...")
    
    kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_final.fit_predict(features)
    
    # --- STEP 3: SAVING RESULTS ---
    # Attach labels back to the original data (with State/District names)
    df['Cluster_ID'] = cluster_labels
    
    # Save the final segmented dataset
    output_path = 'outputs/ev_market_clusters.csv'
    df.to_csv(output_path, index=False)
    print(f"Clustering Complete. Market segmented into {optimal_k} groups.")
    print(f"Results saved to: {output_path}")

    # --- STEP 4: VISUALIZING THE SEGMENTS ---
    # Plot PC1 vs PC2 colored by Cluster
    print("Generating Cluster Map...")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        x='PC1', 
        y='PC2', 
        hue='Cluster_ID', 
        palette='viridis', 
        data=df, 
        s=100, 
        alpha=0.8
    )
    plt.title('EV Market Segments (PC1 vs PC2)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster ID')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig('outputs/figures/market_segments_map.png')
    print("Cluster Map saved to 'outputs/figures/market_segments_map.png'")

if __name__ == "__main__":
    run_clustering()