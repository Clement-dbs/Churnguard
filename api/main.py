from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import pandas as pd
import mlflow
from schemas import PredictionRequest, PredictionResponse
from schemas import compute_risk
import os
import glob


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))

# Trouve le MLmodel le plus récent dans les mlruns montés
mlmodel_paths = glob.glob("/app/mlruns/**/MLmodel", recursive=True)
logger.info(f"MLmodel trouvés : {mlmodel_paths}")

mlmodel_paths.sort(key=os.path.getmtime, reverse=True)
model_dir = os.path.dirname(mlmodel_paths[0])
logger.info(f"Chargement du modèle depuis : {model_dir}")

model = mlflow.pyfunc.load_model(model_dir)

app = FastAPI(title="Churnguard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Churnguard API !",
        "docs": "Visit http://localhost:8000/docs for interactive API documentation",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        df = pd.DataFrame([request.model_dump()])
        sklearn_pipeline = model._model_impl.sklearn_model
        proba = sklearn_pipeline.predict_proba(df)[0][1]
        pred = proba > 0.5
        risk = compute_risk(proba)

        return PredictionResponse(
            churn=bool(pred), churn_probability=float(proba), risk_level=risk
        )
    except Exception as e:
        logger.error(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "model": "churnguard",
        "version": os.path.basename(os.path.dirname(model_dir)),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
