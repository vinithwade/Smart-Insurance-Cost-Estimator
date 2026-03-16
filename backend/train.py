"""
Training script for the insurance cost prediction model.
Trains both Random Forest and XGBoost, saves the best model.
"""
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

from model import build_model, build_preprocessor, NUMERIC_FEATURES, CATEGORICAL_FEATURES

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "dataset" / "insurance_extended.csv"
MODEL_DIR = PROJECT_ROOT / "model"


def load_and_prepare_data():
    """Load extended dataset. Run prepare_data.py first if it doesn't exist."""
    if not DATA_PATH.exists():
        from prepare_data import prepare_extended_dataset
        prepare_extended_dataset()
    
    df = pd.read_csv(DATA_PATH)
    
    # Ensure column names match
    if "children" in df.columns and "dependents" not in df.columns:
        df = df.rename(columns={"children": "dependents"})
    if "sex" in df.columns and "gender" not in df.columns:
        df = df.rename(columns={"sex": "gender"})
    
    # Filter to required columns
    required = NUMERIC_FEATURES + CATEGORICAL_FEATURES + ["charges"]
    df = df[[c for c in required if c in df.columns]]
    
    X = df.drop(columns=["charges"])
    y = df["charges"]
    
    return X, y


def train_and_evaluate():
    """Train models and save the best one."""
    MODEL_DIR.mkdir(exist_ok=True)
    
    X, y = load_and_prepare_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    best_score = -1
    best_model = None
    best_name = ""
    
    for name, model_type in [("xgboost", "xgboost"), ("random_forest", "random_forest")]:
        try:
            pipeline = build_model(model_type)
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            score = r2_score(y_test, y_pred)
            print(f"{name}: R² = {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_model = pipeline
                best_name = name
        except Exception as e:
            print(f"{name}: Failed - {e}")
    
    if best_model is not None:
        model_path = MODEL_DIR / "insurance_model.pkl"
        joblib.dump(best_model, model_path)
        print(f"\nBest model ({best_name}) saved to {model_path}")
        print(f"R² Score: {best_score:.4f}")
    
    return best_model, best_score


if __name__ == "__main__":
    train_and_evaluate()
