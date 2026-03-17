"""
FastAPI backend for Smart Insurance Cost Estimator.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from predict import predict as run_prediction

app = FastAPI(
    title="Smart Insurance Cost Estimator",
    description="ML-powered health insurance premium estimation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://localhost:5173",
        "http://127.0.0.1:3000", "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    gender: str = Field(..., pattern="^(male|female|Male|Female)$")
    height: float = Field(..., gt=0, le=250)  # cm
    weight: float = Field(..., gt=0, le=300)   # kg
    marital_status: Optional[str] = "single"
    dependents: int = Field(..., ge=0, le=20)
    smoker: str = Field(..., pattern="^(yes|no|Yes|No)$")
    alcohol: str = Field(..., pattern="^(never|occasionally|often)$")
    exercise: str = Field(..., pattern="^(none|weekly|daily)$")
    diet: str = Field(..., pattern="^(veg|non-veg|mixed)$")
    diabetes: str = Field(..., pattern="^(yes|no|Yes|No)$")
    heart_problems: Optional[str] = "no"
    chronic_disease: Optional[str] = "no"
    income: int = Field(..., ge=0)
    savings: int = Field(..., ge=0)


@app.get("/")
def root():
    return {"message": "Smart Insurance Cost Estimator API", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/predict")
def predict_premium(request: PredictionRequest):
    """Predict insurance cost from user input."""
    try:
        # Calculate BMI: weight (kg) / height (m)^2
        height_m = request.height / 100
        bmi = round(request.weight / (height_m ** 2), 2)
        
        user_data = {
            "age": request.age,
            "gender": request.gender,
            "bmi": bmi,
            "dependents": request.dependents,
            "smoker": request.smoker,
            "exercise": request.exercise,
            "alcohol": request.alcohol,
            "diet": request.diet,
            "diabetes": request.diabetes,
            "income": request.income,
            "savings": request.savings,
        }
        
        result = run_prediction(user_data)
        result["bmi"] = bmi
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail="Model not trained. Run train.py first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
