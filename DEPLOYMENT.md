# Deployment Guide

## 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Smart Insurance Cost Estimator"
git branch -M main
git remote add origin https://github.com/vinithwade/Smart-Insurance-Cost-Estimator.git
git push -u origin main
```

## 2. Deploy Backend (Render)

The backend must be deployed first so you have the API URL for the frontend.

1. Go to [render.com](https://render.com) and sign in
2. **New** → **Web Service**
3. Connect your GitHub repo: `vinithwade/Smart-Insurance-Cost-Estimator`
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python prepare_data.py && python train.py`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**
6. Wait for deploy, then copy your backend URL (e.g. `https://insurance-estimator-api.onrender.com`)

## 3. Deploy Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) and sign in
2. **Add New** → **Project**
3. Import `vinithwade/Smart-Insurance-Cost-Estimator`
4. Configure:
   - **Root Directory**: `frontend` (click Edit, set to `frontend`)
   - **Environment Variable**: Add `VITE_API_URL` = your Render backend URL (e.g. `https://insurance-estimator-api.onrender.com` — no trailing slash)
5. Click **Deploy**

Your app will be live at the Vercel URL (e.g. `https://smart-insurance-cost-estimator.vercel.app`).

## Notes

- **Render free tier**: Backend may spin down after 15 min of inactivity. First request after idle can take ~30–60 seconds.
- **CORS**: The backend allows requests from Vercel domains. If you use a custom domain, update `app.py` CORS origins.
