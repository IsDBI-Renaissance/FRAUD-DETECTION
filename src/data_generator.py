import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import random
from typing import Dict, List

fake = Faker()

def generate_islamic_transactions(num_transactions: int = 10000, fraud_ratio: float = 0.01) -> pd.DataFrame:
    """Generate synthetic Islamic financial transactions with fraud patterns"""
    transaction_types = [
        'Murabaha', 'Ijarah', 'Mudarabah', 'Musharakah', 
        'Sukuk', 'Qard', 'Tawarruq', 'Istisna'
    ]
    
    institutions = [
        'Al Rajhi Bank', 'Dubai Islamic Bank', 'Kuwait Finance House',
        'Qatar Islamic Bank', 'Maybank Islamic', 'Al Baraka Bank'
    ]
    
    data = []
    fraud_indices = set(random.sample(range(num_transactions), int(num_transactions * fraud_ratio)))
    
    for i in range(num_transactions):
        is_fraud = i in fraud_indices
            
        transaction = {
            'transaction_id': f'TXN{fake.unique.random_number(digits=8)}',
            'date': fake.date_between(start_date='-1y', end_date='today'),
            'type': random.choice(transaction_types),
            'amount': abs(np.random.lognormal(mean=5, sigma=1.5)),
            'currency': random.choice(['USD', 'SAR', 'AED', 'MYR', 'QAR']),
            'institution': random.choice(institutions),
            'counterparty': fake.company(),
            'location': fake.country(),
            'is_fraud': is_fraud
        }
        
        if is_fraud:
            fraud_pattern = random.choice([
                'round_tripping', 'fake_commodity', 'gharar_excessive',
                'riba_disguised', 'misrepresented_asset', 'wash_trading'
            ])
            
            if fraud_pattern == 'round_tripping':
                transaction['amount'] *= random.uniform(0.9, 1.1)
                transaction['counterparty'] = 'Shell Company ' + fake.company_suffix()
            elif fraud_pattern == 'fake_commodity':
                transaction['type'] = 'Murabaha'
                transaction['description'] = 'Fictitious commodity transaction'
            elif fraud_pattern == 'gharar_excessive':
                transaction['amount'] *= random.uniform(5, 10)
                transaction['description'] = 'Excessive uncertainty in contract'
            elif fraud_pattern == 'riba_disguised':
                transaction['type'] = random.choice(['Tawarruq', 'Inah'])
                transaction['description'] = 'Potential disguised interest'
            elif fraud_pattern == 'misrepresented_asset':
                transaction['type'] = 'Ijarah'
                transaction['description'] = 'Asset not as described'
            elif fraud_pattern == 'wash_trading':
                transaction['amount'] = round(transaction['amount'], -3)
                transaction['counterparty'] = 'Related Party ' + fake.company_suffix()
                
            transaction['fraud_pattern'] = fraud_pattern
        else:
            transaction['description'] = 'Normal transaction'
            transaction['fraud_pattern'] = None
            
        data.append(transaction)
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['hour'] = np.random.randint(8, 18, size=len(df))
    
    df['amount_log'] = np.log(df['amount'] + 1)
    df['amount_category'] = pd.cut(df['amount'], 
                                 bins=[0, 1000, 10000, 100000, float('inf')],
                                 labels=['small', 'medium', 'large', 'xlarge'])
    
    counterparty_counts = df['counterparty'].value_counts().to_dict()
    df['counterparty_freq'] = df['counterparty'].map(counterparty_counts)
    
    return df
