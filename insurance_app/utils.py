# utils.py

import json
import pandas as pd
from datetime import datetime

def load_data(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, default=str)

def load_csv_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return pd.DataFrame()

def calculate_claim_frequency(claims):
    return len(claims)

def is_high_risk(claims, sum_insured):
    this_year = datetime.now().year
    total_claimed = sum([float(c["amount"]) for c in claims])
    recent_claims = [c for c in claims if datetime.strptime(c["date"], "%Y-%m-%d").year == this_year]
    return len(recent_claims) > 3 or total_claimed > 0.8 * float(sum_insured)

def aggregate_by_policy_type(policyholders):
    df = pd.DataFrame(policyholders)
    return df['policy_type'].value_counts()

def total_claims_per_month(claims):
    df = pd.DataFrame(claims)
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.strftime('%Y-%m')).size()

def average_claim_by_type(policyholders, claims):
    ph_df = pd.DataFrame(policyholders)
    cl_df = pd.DataFrame(claims)
    merged = cl_df.merge(ph_df[['id', 'policy_type']], left_on='policyholder_id', right_on='id')
    return merged.groupby('policy_type')['amount'].mean()

def highest_claim(claims):
    return max(claims, key=lambda c: float(c['amount']), default=None)

def get_pending_claims(claims):
    return [c for c in claims if c["status"].lower() == "pending"]
