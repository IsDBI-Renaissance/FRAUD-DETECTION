# Islamic Fraud Detection System

## Overview
This project leverages cutting-edge machine learning techniques to detect fraudulent transactions in Islamic financial operations. The model is trained using advanced algorithms like Random Forest to analyze transaction features and predict the likelihood of fraud, ensuring compliance with Islamic financial standards. The API built with FastAPI allows users to interact with the system seamlessly.

## Features
- Machine learning-based fraud detection specifically tailored for Islamic financial transactions
- Highly accurate prediction capabilities based on transaction characteristics
- FastAPI integration for seamless API interactions
- Support for various Islamic financial transaction types

## Project Structure
```
islamic_fraud_api/
├── api.py                 # FastAPI application to handle requests
├── model.py               # Fraud detection model with training and prediction functionality
├── train_model.py         # Script to train the model
├── requirements.txt       # Dependencies for the project
└── models/
    └── fraud_detector.joblib  # Pre-trained fraud detection model
```

### Files Overview
1. **`api.py`**: The FastAPI application that handles incoming requests, processes transaction data, and returns fraud predictions.
2. **`model.py`**: Contains the `IslamicFraudDetector` class with methods to train the model, load the trained model, and predict fraud.
3. **`train_model.py`**: Script to train the model from a given dataset.
4. **`requirements.txt`**: Contains the list of dependencies needed to run the application.
5. **`models/fraud_detector.joblib`**: The trained Random Forest model used for predicting fraud.

## Installation

To install the necessary dependencies, create a virtual environment (optional but recommended) and run:

```bash
pip install -r requirements.txt
```

## Model Training

Before running the API, you must train the model:

```bash
python train_model.py
```

This will train the model using the `transactions.csv` file and save the trained model as `models/fraud_detector.joblib`.

## Running the FastAPI Application

After the model is trained, start the FastAPI server:

```bash
python api.py
```

The API will be accessible at http://localhost:8000.

## API Documentation

### POST /detect-fraud

**Description:**
This endpoint receives transaction details and predicts whether the transaction is fraudulent based on the trained model.

**Input Format:**
```json
{
  "transaction_id": "TXN123",
  "date": "2023-05-15",
  "type": "Murabaha",
  "amount": 150000,
  "currency": "USD",
  "institution": "Al Rajhi Bank",
  "counterparty": "Shell Company LLC",
  "location": "Cayman Islands"
}
```

**Parameters:**
- `transaction_id` (str): Unique identifier for the transaction
- `date` (str): Transaction date in YYYY-MM-DD format
- `type` (str): Type of Islamic financial transaction (e.g., Murabaha, Ijarah)
- `amount` (float): Amount of money involved
- `currency` (str): Currency used (e.g., USD, SAR)
- `institution` (str): Name of the financial institution
- `counterparty` (str): Company or entity on the other side
- `location` (str): Geographical location of the transaction

**Output Format:**
```json
{
  "transaction_id": "TXN123",
  "fraud_probability": 0.75,
  "is_fraud": true,
  "features_used": {
    "amount_log": 11.92,
    "day_of_week": 1,
    "month": 5
  }
}
```

**Response Fields:**
- `transaction_id` (str): The transaction's unique identifier
- `fraud_probability` (float): Probability that the transaction is fraudulent
- `is_fraud` (bool): Prediction result (true = fraudulent, false = legitimate)
- `features_used` (object): Features used by the model for the prediction

## Example Usage

**Request:**
```bash
curl -X POST "http://localhost:8000/detect-fraud" \
-H "Content-Type: application/json" \
-d '{
  "transaction_id": "TXN123",
  "date": "2023-05-15",
  "type": "Murabaha",
  "amount": 150000,
  "currency": "USD",
  "institution": "Al Rajhi Bank",
  "counterparty": "Shell Company LLC",
  "location": "Cayman Islands"
}'
```

**Response:**
```json
{
  "transaction_id": "TXN123",
  "fraud_probability": 0.75,
  "is_fraud": true,
  "features_used": {
    "amount_log": 11.92,
    "day_of_week": 1,
    "month": 5
  }
}
```

## Quick Start Guide

1. **Train the Model**
   ```bash
   python train_model.py
   ```

2. **Start the FastAPI Server**
   ```bash
   python api.py
   ```

3. **Test the API**
   Send a POST request to http://localhost:8000/detect-fraud with a JSON payload as described above.

## Requirements
- Python 3.8+
- FastAPI
- scikit-learn
- joblib
- pandas
- numpy

