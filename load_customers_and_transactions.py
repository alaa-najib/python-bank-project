import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys

# 🔧 DB connection
DATABASE_URL  = "postgresql://postgres:pg123456@localhost:5432/bank"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# ✅ Load everything inside a DB transaction
def load_customers_safely():
    session = Session()
    try:
        # Load customers
        print("Reading customers.csv...")
        customers_df = pd.read_csv("./data/sebank_customers_with_accounts.csv")
        if "created_at" in customers_df.columns:
            customers_df["created_at"] = pd.to_datetime(customers_df["created_at"], errors="coerce")
        customers_df.to_sql("customers", con=engine, if_exists="append", index=False, method="multi")

        session.commit()
        print("All data loaded successfully.")

    except Exception as e:
        session.rollback()
        print("Error occurred. Rolled back all operations.")
        print(f"Error details: {e}", file=sys.stderr)

    finally:
        session.close()

def load_accounts_and_transactions_safely():
    session = Session()
    try:
        # Load transactions
        print("Reading transactions.csv...")
        transactions_df = pd.read_csv("./data/transactions.csv")
        transactions_df["timestamp"] = pd.to_datetime(transactions_df["timestamp"], errors="coerce")

        # Extract unique accounts
        print("Extracting unique accounts...")
        senders = transactions_df[["sender_account"]].rename(columns={"sender_account": "account_id"})
        receivers = transactions_df[["receiver_account"]].rename(columns={"receiver_account": "account_id"})
        accounts_df = pd.concat([senders, receivers]).drop_duplicates().dropna()
        accounts_df["currency"] = "SEK"
        accounts_df["created_at"] = datetime.utcnow()

        # Insert accounts
       # accounts_df.to_sql("accounts", con=engine, if_exists="append", index=False, method="multi")

        # Insert transactions
        transactions_df.to_sql("transactions", con=engine, if_exists="append", index=False, method="multi")

        session.commit()
        print("All data loaded successfully.")

    except Exception as e:
        session.rollback()
        print("Error occurred. Rolled back all operations.")
        print(f"Error details: {e}", file=sys.stderr)

    finally:
        session.close()

if __name__ == "__main__":
    load_data_safely()
