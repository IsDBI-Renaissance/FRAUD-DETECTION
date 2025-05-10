from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import IslamicFraudDetector

app = FastAPI()

# Load the pre-trained fraud detection model
detector = IslamicFraudDetector.load("models/fraud_detector.joblib")

class Transaction(BaseModel):
    transaction_id: str
    date: str
    type: str
    amount: float
    currency: str
    institution: str
    counterparty: str
    location: str

@app.post("/detect-fraud")
async def detect_fraud(transaction: Transaction):
    transaction_dict = transaction.dict()
    
    # Use the trained model to make a prediction
    try:
        result = detector.predict(transaction_dict)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
