import os

def secure_project():
    # 1. Create the .env file with placeholders
    env_content = """# Kaggle API Credentials
# Get these from your Kaggle Account -> Settings -> API -> Create New Token
KAGGLE_USERNAME=paste_your_username_here
KAGGLE_KEY=paste_your_api_key_here
"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("[Success] Created '.env' file.")
    else:
        print("[Info] '.env' file already exists. Skipping creation to avoid overwriting keys.")

    # 2. Update .gitignore to exclude .env and data
    gitignore_entry = "\n# Security & Data\n.env\n.ipynb_checkpoints/\ndata/\n__pycache__/\n"
    
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            current_content = f.read()
        
        if ".env" not in current_content:
            with open(".gitignore", "a") as f:
                f.write(gitignore_entry)
            print("[Success] Added '.env' to .gitignore.")
        else:
            print("[Info] '.gitignore' is already configured.")
    else:
        with open(".gitignore", "w") as f:
            f.write(gitignore_entry)
        print("[Success] Created '.gitignore'.")

    print("\nACTION REQUIRED: Open the '.env' file now and paste your actual Kaggle credentials.")

if __name__ == "__main__":
    secure_project()