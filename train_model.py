import pandas as pd
from model import IslamicFraudDetector

# Load your transaction data
df = pd.read_csv('transactions.csv')

# Train the model
detector = IslamicFraudDetector()
detector.train(df)

# Save the trained model
detector.save("models/fraud_detector.joblib")
