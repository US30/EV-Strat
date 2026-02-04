import os

def create_project_structure():
    # 1. Define the directory structure
    directories = [
        "data/raw",
        "data/processed",
        "src",
        "notebooks",
        "outputs/figures",
        "outputs/reports"
    ]

    # 2. Create directories
    print("Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  - Created: {directory}")

    # 3. Define environment.yml content
    yaml_content = """name: ev_strat_env
channels:
  - defaults
dependencies:
  - python=3.9
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - seaborn
  - jupyter
  - pip
"""

    # 4. Write the environment file
    with open("environment.yml", "w") as f:
        f.write(yaml_content)
    
    print("\n[Success] Project structure created and 'environment.yml' generated.")
    print("Next Steps:")
    print("1. Run: conda env create -f environment.yml")
    print("2. Run: conda activate ev_strat_env")

if __name__ == "__main__":
    create_project_structure()