import os
os.environ["PREFECT_API_ENABLE_HTTP2"] = "false"
os.environ["REQUESTS_CA_BUNDLE"] = ""


from prefect import flow, task, get_run_logger
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Import your custom modules
from validate_transactions import validate_transaction
from load_customers_and_transactions import load_customers_safely, load_accounts_and_transactions_safely

# Database setup
DATABASE_URL = "postgresql://postgres:pg123456@localhost:5432/bank"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@task
def log_step(step: str, message: str, status: str):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO logs (step, message, status, timestamp) VALUES (:s, :m, :st, :t)"),
            {"s": step, "m": message, "st": status, "t": datetime.utcnow()}
        )

@flow(name="Bank Transaction Workflow")
def transaction_pipeline():
    logger = get_run_logger()
    session = Session()

    report = {
        "valid_transactions": 0,
        "invalid_transactions": 0,
        "total": 0
    }

    try:
        log_step.submit("load_customers", "Loading customers", "started")
        load_customers_safely()
        log_step.submit("load_customers", "Customers loaded", "success")

        # Load and process transactions
        log_step.submit("load_transactions", "Loading transactions.csv", "started")
        df = pd.read_csv("./data/transactions.csv")
        report["total"] = len(df)

        load_accounts_and_transactions_safely()
        log_step.submit("load_accounts", "Accounts inserted", "success")

        valid_rows, invalid_rows = [], []
        for _, row in df.iterrows():
            is_valid, error = validate_transaction(row)
            if is_valid:
                valid_rows.append(row)
            else:
                invalid_rows.append({
                    "transaction_id": row.get("transaction_id"),
                    "raw_data": json.dumps(row.dropna().to_dict()),
                    "error_message": error,
                    "detected_at": datetime.utcnow()
                })

        if valid_rows:
            pd.DataFrame(valid_rows).to_sql("transactions", con=engine, if_exists="append", index=False)
            report["valid_transactions"] = len(valid_rows)
            log_step.submit("insert_valid", f"{len(valid_rows)} valid transactions", "success")

        if invalid_rows:
            pd.DataFrame(invalid_rows).to_sql("invalid_transactions", con=engine, if_exists="append", index=False)
            report["invalid_transactions"] = len(invalid_rows)
            log_step.submit("insert_invalid", f"{len(invalid_rows)} invalid transactions", "warning")

        session.commit()
        logger.info("✅ Workflow complete")
        logger.info(json.dumps(report, indent=2))

    except Exception as e:
        session.rollback()
        log_step.submit("workflow_error", str(e), "error")
        logger.error(f"❌ Workflow failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    transaction_pipeline()
