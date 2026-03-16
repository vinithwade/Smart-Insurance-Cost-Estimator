"""
Extends the insurance dataset with additional columns for the full ML pipeline.
Adds: exercise, alcohol, diet, diabetes, income, savings
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "dataset" / "insurance.csv"
OUTPUT_PATH = PROJECT_ROOT / "dataset" / "insurance_extended.csv"


def prepare_extended_dataset():
    """Load base dataset and add synthetic columns that correlate with insurance costs."""
    df = pd.read_csv(DATA_PATH)
    
    np.random.seed(42)
    n = len(df)
    
    # Exercise: correlates with lower BMI (healthier = more exercise)
    exercise_options = ["none", "weekly", "daily"]
    exercise_probs = []
    for bmi in df["bmi"]:
        if bmi > 30:
            exercise_probs.append([0.5, 0.35, 0.15])
        elif bmi > 25:
            exercise_probs.append([0.3, 0.5, 0.2])
        else:
            exercise_probs.append([0.2, 0.4, 0.4])
    df["exercise"] = [np.random.choice(exercise_options, p=p) for p in exercise_probs]
    
    # Alcohol: smokers more likely to drink often
    alcohol_options = ["never", "occasionally", "often"]
    alcohol_probs = []
    for smoker in df["smoker"]:
        alcohol_probs.append([0.1, 0.4, 0.5] if smoker == "yes" else [0.4, 0.45, 0.15])
    df["alcohol"] = [np.random.choice(alcohol_options, p=p) for p in alcohol_probs]
    
    # Diet: veg, non-veg, mixed
    diet_options = ["veg", "non-veg", "mixed"]
    df["diet"] = np.random.choice(diet_options, n, p=[0.25, 0.35, 0.4])
    
    # Diabetes: higher with age and BMI
    diabetes_prob = 0.05 + 0.002 * df["age"] + 0.01 * (df["bmi"] - 25).clip(0, 20)
    diabetes_prob = np.clip(diabetes_prob, 0.05, 0.5)
    df["diabetes"] = np.where(np.random.random(n) < diabetes_prob, "yes", "no")
    
    # Income: correlates with age (older = higher income), add some randomness
    base_income = 300000 + df["age"] * 8000 + np.random.normal(0, 100000, n)
    df["income"] = np.clip(base_income, 100000, 2000000).astype(int)
    
    # Savings: 15-40% of income
    savings_ratio = 0.15 + np.random.uniform(0, 0.25, n)
    df["savings"] = (df["income"] * savings_ratio).astype(int)
    
    # Rename for consistency: sex -> gender, children -> dependents
    df = df.rename(columns={"sex": "gender", "children": "dependents"})
    
    # Reorder columns
    cols = ["age", "gender", "bmi", "dependents", "smoker", "exercise", "alcohol", 
            "diet", "diabetes", "region", "income", "savings", "charges"]
    df = df[cols]
    
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Extended dataset saved to {OUTPUT_PATH}")
    print(f"Shape: {df.shape}")
    return df


if __name__ == "__main__":
    prepare_extended_dataset()
