"""
ML model definitions and preprocessing pipeline for insurance cost prediction.
Uses Random Forest and XGBoost with proper preprocessing.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

# Feature configuration
NUMERIC_FEATURES = ["age", "bmi", "income", "savings", "dependents"]
CATEGORICAL_FEATURES = ["gender", "smoker", "exercise", "diet", "alcohol", "diabetes"]

# Map user input to model expected values
GENDER_MAP = {"male": "male", "female": "female", "Male": "male", "Female": "female"}
SMOKER_MAP = {"yes": "yes", "no": "no", "Yes": "yes", "No": "no"}
EXERCISE_MAP = {"none": "none", "weekly": "weekly", "daily": "daily"}
ALCOHOL_MAP = {"never": "never", "occasionally": "occasionally", "often": "often"}
DIET_MAP = {"veg": "veg", "non-veg": "non-veg", "mixed": "mixed"}
DIABETES_MAP = {"yes": "yes", "no": "no", "Yes": "yes", "No": "no"}


def build_preprocessor():
    """Build the preprocessing pipeline."""
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def build_model(model_type="xgboost"):
    """Build the ML model. Default: XGBoost, fallback: Random Forest."""
    preprocessor = build_preprocessor()
    
    if model_type == "xgboost" and HAS_XGB:
        regressor = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
        )
    else:
        regressor = RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            random_state=42,
        )
    
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", regressor),
    ])
    return pipeline


def get_risk_category(cost: float) -> str:
    """Classify risk based on predicted cost (in INR)."""
    # Thresholds scaled for INR (US dataset * ~83 conversion)
    if cost < 300000:
        return "LOW"
    elif cost < 600000:
        return "MEDIUM"
    else:
        return "HIGH"


def get_lifestyle_suggestions(data: dict) -> list[str]:
    """Generate lifestyle suggestions based on user inputs."""
    suggestions = []
    
    if data.get("smoker", "").lower() == "yes":
        suggestions.append("Smoking significantly increases insurance costs. Consider quitting to reduce premiums.")
    
    bmi = data.get("bmi")
    if bmi is not None:
        if bmi > 30:
            suggestions.append("Your BMI indicates obesity. Regular exercise and a balanced diet can help reduce health risks.")
        elif bmi > 25:
            suggestions.append("Your BMI is slightly elevated. Consider increasing physical activity to reach a healthier range.")
    
    exercise = data.get("exercise", "").lower()
    if exercise == "none":
        suggestions.append("Start with 30 minutes of walking daily. Regular exercise can lower insurance costs.")
    
    alcohol = data.get("alcohol", "").lower()
    if alcohol == "often":
        suggestions.append("Reducing alcohol intake can improve your health profile and potentially lower premiums.")
    elif alcohol == "occasionally":
        suggestions.append("Moderate alcohol consumption is fine. Keep it in check.")
    
    diet = data.get("diet", "").lower()
    if diet == "non-veg":
        suggestions.append("Consider a balanced mixed or plant-based diet for better cardiovascular health.")
    
    if data.get("diabetes", "").lower() == "yes":
        suggestions.append("Manage diabetes with regular check-ups and medication adherence. This helps control long-term costs.")
    
    if not suggestions:
        suggestions.append("You're on a good track! Maintain your healthy lifestyle habits.")
    
    return suggestions
