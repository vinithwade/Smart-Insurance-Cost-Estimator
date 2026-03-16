# Smart Insurance Cost Estimator

ML-powered health insurance premium estimation using Random Forest and XGBoost.

## Features

- **Multi-step assessment**: Personal info → Lifestyle → Health → Financial
- **BMI calculation** from height and weight
- **ML prediction**: Random Forest / XGBoost models
- **Risk classification**: Low / Medium / High
- **Lifestyle suggestions** based on your profile

## Quick Start

### 1. Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python prepare_data.py    # Extend dataset with exercise, alcohol, diet, etc.
python train.py          # Train model (Random Forest + XGBoost)
uvicorn app:app --reload --port 8000
```

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The frontend proxies `/api` to the backend.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for pushing to GitHub and hosting on Vercel + Render.

## Project Structure

```
insurance-estimator/
├── backend/
│   ├── app.py          # FastAPI server
│   ├── model.py       # ML pipeline
│   ├── train.py       # Training script
│   ├── predict.py     # Prediction logic
│   └── prepare_data.py
├── dataset/
│   ├── insurance.csv
│   └── insurance_extended.csv
├── model/
│   └── insurance_model.pkl
└── frontend/
    └── (React app)
```

## API

- `POST /api/predict` — Get insurance estimate

Request body: `age`, `gender`, `height`, `weight`, `dependents`, `smoker`, `alcohol`, `exercise`, `diet`, `diabetes`, `income`, `savings`
