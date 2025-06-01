## 📥 Data Loader Script (PostgreSQL)

This script loads cleaned data from CSV files into the PostgreSQL database using SQLAlchemy and pandas.

### 📦 Dependencies

Make sure you have these Python packages installed:

```bash
pip install pandas sqlalchemy psycopg2
```

---

### 🧰 What the Script Does

1. Connects to the PostgreSQL database using SQLAlchemy.
2. Loads the `transactions.csv` file from the `./data` directory.
3. Converts the `timestamp` field to datetime format.
4. Extracts unique bank accounts from both sender and receiver fields.
5. Inserts the processed data into the `transactions` table (and optionally `accounts`).
6. Wraps all operations inside a **database transaction**, with full rollback support on failure.

---

### ⚠️ Notes

- The customer data section is commented out but can be activated as needed.
- Insert to `accounts` is also commented to avoid duplication during testing.
- The script ensures safe operations using `try/except/finally` and commits only if all steps succeed.

---

### ▶️ How to Run

Ensure your PostgreSQL server is running and the database schema has been created. Then run:

```bash
python load_customers_and_transactions.py
```
