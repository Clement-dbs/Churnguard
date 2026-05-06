from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import pandas as pd
import mlflow
from mlflow import MlflowClient
from schemas import PredictionRequest, PredictionResponse
from schemas import compute_risk


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

mlflow.set_tracking_uri("file:./mlruns")
model = mlflow.pyfunc.load_model("models:/churnguard/Production")

app = FastAPI(
    title="Churnguard API",
    version="1.0.0"
)

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
        "docs": "Visit http://localhost:8000/docs for interactive API documentation"
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
            churn=bool(pred),
            churn_probability=float(proba),
            risk_level=risk
        )
    except Exception as e:  
        logger.error(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", tags=["Health"])
def health_check():

    client = MlflowClient()
    latest = client.get_latest_versions("churnguard", stages=["Production"])[0].version

    return {
        "status": "ok",
        "model" : "churnguard",
        "version": latest
    }

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
