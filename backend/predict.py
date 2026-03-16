"""
Prediction module - loads model and predicts insurance cost from user input.
"""
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from model import get_risk_category, get_lifestyle_suggestions

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODEL_PATH = PROJECT_ROOT / "model" / "insurance_model.pkl"

# Convert USD to INR (approximate)
USD_TO_INR = 83.0


def load_model():
    """Load the trained model."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run train.py first."
        )
    return joblib.load(MODEL_PATH)


def predict(user_data: dict) -> dict:
    """
    Predict insurance cost from user input.
    user_data should contain: age, gender, bmi, dependents, smoker, exercise, alcohol, diet, diabetes, income, savings
    """
    model = load_model()
    
    # Build DataFrame with correct column order
    df = pd.DataFrame([{
        "age": int(user_data.get("age", 30)),
        "gender": str(user_data.get("gender", "male")).lower(),
        "bmi": float(user_data.get("bmi", 25)),
        "dependents": int(user_data.get("dependents", 0)),
        "smoker": str(user_data.get("smoker", "no")).lower(),
        "exercise": str(user_data.get("exercise", "weekly")).lower(),
        "alcohol": str(user_data.get("alcohol", "occasionally")).lower(),
        "diet": str(user_data.get("diet", "mixed")).lower(),
        "diabetes": str(user_data.get("diabetes", "no")).lower(),
        "income": int(user_data.get("income", 500000)),
        "savings": int(user_data.get("savings", 100000)),
    }])
    
    # Model was trained on USD charges - convert prediction to INR
    cost_usd = float(model.predict(df)[0])
    cost_inr = round(cost_usd * USD_TO_INR, 2)
    
    income = int(user_data.get("income", 500000))
    savings = int(user_data.get("savings", 100000))
    risk = get_risk_category(income, savings)
    suggestions = get_lifestyle_suggestions(user_data)
    
    return {
        "estimated_cost": float(cost_inr),
        "estimated_cost_usd": float(round(cost_usd, 2)),
        "risk_category": str(risk),
        "suggestions": [str(s) for s in suggestions],
        "bmi": float(user_data.get("bmi")) if user_data.get("bmi") is not None else None,
    }
