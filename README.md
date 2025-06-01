
# 🏦 Bank Data Quality Pipeline with Prefect

This project implements a robust, automated data quality workflow using [Prefect](https://docs.prefect.io/), PostgreSQL, and Python. It processes large volumes of bank transaction data with validation, error handling, and logging.

---

## 📂 Project Structure

```
bank_project/
├── customers.csv                          # Input: customer data
├── transactions.csv                       # Input: transaction data
├── validate_transactions.py               # Contains row validation logic
├── load_customers_and_transactions.py     # Contains customer/account loading logic
├── pipeline.py                            # Prefect flow: orchestrates the entire process
```

---

## ⚙️ Workflow Overview

The pipeline is orchestrated using **Prefect 2.x/3.x** and includes the following steps:

### ✅ Step-by-Step Logic

| Step                       | Description |
|----------------------------|-------------|
| **1. Load Customers**      | Reads `customers.csv` and inserts records into the `customers` table. |
| **2. Load Transactions**   | Reads `transactions.csv` and prepares for validation and processing. |
| **3. Extract Accounts**    | Extracts all unique sender/receiver accounts from `transactions.csv` and stores them in the `accounts` table. |
| **4. Validate Transactions** | Each transaction is validated for structure, required fields, and formatting using `validate_transaction()` in `validate_transactions.py`. |
| **5. Insert Valid Data**   | Valid rows are inserted into the `transactions` table. |
| **6. Store Invalid Data**  | Invalid rows are logged to the `invalid_transactions` table with error messages. |
| **7. Log Workflow Events** | Every major step is logged to the `logs` table using the Prefect `log_step()` task. |
| **8. Final Report**        | A summary of total, valid, and invalid transactions is printed to the console. |

---

## 🐍 Running the Pipeline

### Install Dependencies
```bash
pip install prefect pandas sqlalchemy psycopg2-binary
```

### Run the Flow
```bash
python pipeline.py
```

This will execute the full workflow and print a report like:
```json
{
  "valid_transactions": 89500,
  "invalid_transactions": 10500,
  "total": 100000
}
```

---

## 🧠 What’s Being Validated?

Validation checks:
- Required fields: `transaction_id`, `timestamp`, `amount`, `currency`, `sender_account`, `receiver_account`
- Timestamp and numeric formatting
- Empty/null values

Invalid rows are safely redirected to the `invalid_transactions` table for review and are not loaded into production tables.

---

## 📦 Tables Used

| Table Name             | Purpose                                   |
|------------------------|-------------------------------------------|
| `customers`            | Stores customer profiles                  |
| `accounts`             | Stores all sender/receiver account IDs    |
| `transactions`         | Stores only valid transactions            |
| `invalid_transactions` | Stores rows that failed validation        |
| `logs`                 | Workflow event tracking and error logging |

---

## ✅ Next Steps

- [ ] Add reporting to CSV or dashboard
- [ ] Schedule daily jobs using Prefect Cloud or Prefect Agent
- [ ] Add unit tests for validation logic
- [ ] Integrate notification (Slack/email) on failure

---

## 🙌 Authors

- Workflow automation using **Prefect**
- Data validation using **Pandas**
- Database powered by **PostgreSQL** + **SQLAlchemy**
