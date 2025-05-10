import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from typing import Dict

class IslamicFraudDetector:
    def __init__(self):
        self.model = None
    
    def train(self, df: pd.DataFrame) -> Dict:
        """Train model with automatic feature engineering"""
        if df.empty:
            raise ValueError("Empty DataFrame provided for training")
            
        if 'is_fraud' not in df.columns:
            raise ValueError("DataFrame must contain 'is_fraud' column")
        
        # Feature engineering
        df['amount_log'] = np.log(df['amount'] + 1)
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['month'] = pd.to_datetime(df['date']).dt.month
        
        # Train model
        X = df[['amount_log', 'day_of_week', 'month']]
        y = df['is_fraud']
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',
            random_state=42
        )
        self.model.fit(X, y)
        
        return {"status": "success", "samples": len(df)}

    def save(self, path: str):
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> 'IslamicFraudDetector':
        """Load model from disk"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at {path}")
            
        detector = cls()
        detector.model = joblib.load(path)
        return detector

    def predict(self, transaction: Dict) -> Dict:
        """Predict fraud probability for a transaction"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        # Feature engineering for prediction
        features = {
            'amount_log': np.log(transaction['amount'] + 1),
            'day_of_week': pd.to_datetime(transaction['date']).dayofweek,
            'month': pd.to_datetime(transaction['date']).month
        }
        
        # Predict probability of fraud
        proba = self.model.predict_proba([list(features.values())])[0][1]
        
        # Convert numpy.bool to native Python bool
        return {
            "transaction_id": transaction['transaction_id'],
            "fraud_probability": float(proba),
            "is_fraud": bool(proba > 0.5),  # Convert to native Python bool
            "features_used": features
        }
