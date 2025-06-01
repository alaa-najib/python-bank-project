# validate_transactions.py

import pandas as pd

def validate_transaction(row):
    required_fields = [
        "transaction_id", "timestamp", "amount", "currency",
        "sender_account", "receiver_account"
    ]
    for field in required_fields:
        if pd.isna(row.get(field)):
            return False, f"Missing required field: {field}"
    try:
        float(row["amount"])
        pd.to_datetime(row["timestamp"])
    except Exception as e:
        return False, f"Invalid format: {str(e)}"
    return True, ""
