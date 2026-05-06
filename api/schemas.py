from pydantic import BaseModel, Field
from typing import Literal


class PredictionRequest(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0, 1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int = Field(gt=-1)

    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]

    InternetService: Literal["DSL", "Fiber optic", "No"]

    OnlineSecurity: Literal["Yes", "No"]
    OnlineBackup: Literal["Yes", "No"]
    DeviceProtection: Literal["Yes", "No"]
    TechSupport: Literal["Yes", "No"]
    StreamingTV: Literal["Yes", "No"]
    StreamingMovies: Literal["Yes", "No"]

    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal["Electronic check", "Bank transfer (automatic)", "Mailed check", "Credit card (automatic)"]

    MonthlyCharges: float = Field(gt=0)
    TotalCharges: float = Field(gt=0)

class PredictionResponse(BaseModel):
    churn: bool
    churn_probability: float
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

def compute_risk(prob):
    if prob < 0.3:
        return "LOW"
    elif prob < 0.6:
        return "MEDIUM"
    return "HIGH"

