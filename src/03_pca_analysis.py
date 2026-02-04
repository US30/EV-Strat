import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

def run_pca():
    print("Loading preprocessed data...")
    # Load the data from Phase 2
    input_path = 'data/processed/ev_market_final.csv'
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {input_path}. Did you run 'src/02_preprocessing.py'?")

    # 1. SEPARATE FEATURES AND METADATA
    # We only want to run PCA on the numeric columns, not the names
    metadata_cols = ['State', 'District']
    
    # robustly select all numeric columns that are not metadata
    features = df.select_dtypes(include=[np.number])
    feature_names = features.columns.tolist()
    
    print(f"Features selected for PCA ({len(feature_names)}): {feature_names}")

    # 2. APPLY PCA
    print("Running PCA...")
    # We ask PCA to retain 90% of the useful variance/information
    pca = PCA(n_components=0.90) 
    principal_components = pca.fit_transform(features)
    
    # Get the number of components PCA decided to keep
    n_components = pca.n_components_
    print(f"Reduced dimensions from {features.shape[1]} to {n_components} components.")
    
    # 3. CREATE PCA DATAFRAME
    # Create column names like PC1, PC2, etc.
    pca_cols = [f'PC{i+1}' for i in range(n_components)]
    
    df_pca = pd.DataFrame(data=principal_components, columns=pca_cols)
    
    # Attach the metadata (State/District) back so we know which point is which
    final_df = pd.concat([df[metadata_cols], df_pca], axis=1)
    
    # Save the output for the next phase (Clustering)
    output_path = 'data/processed/pca_output.csv'
    final_df.to_csv(output_path, index=False)
    print(f"PCA Data saved to: {output_path}")

    # 4. VISUALIZATION: SCREE PLOT
    # This proves you selected the right number of components (Resume point!)
    print("Generating Scree Plot...")
    plt.figure(figsize=(10, 6))
    
    # Plot cumulative variance
    plt.plot(range(1, n_components + 1), np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='--')
    plt.title('PCA Scree Plot: Cumulative Variance Explained')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Variance Explained')
    plt.grid(True)
    
    # Save figure (Since you are on Antigravity/Cloud, we save instead of show)
    plot_path = 'outputs/figures/pca_scree_plot.png'
    plt.savefig(plot_path)
    print(f"Scree plot saved to: {plot_path}")

    # 5. INTERPRETATION (OPTIONAL BUT IMPRESSIVE)
    # Print what the first Component (PC1) actually represents
    print("\n--- COMPONENT INTERPRETATION ---")
    loadings = pd.DataFrame(pca.components_.T, columns=pca_cols, index=feature_names)
    print("Top factors driving PC1 (The dominant trend):")
    print(loadings['PC1'].sort_values(ascending=False))

if __name__ == "__main__":
    run_pca()