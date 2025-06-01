# 🏦 Bank Project – Database Schema Overview

This project implements a data quality workflow system for processing financial transactions in a Swedish bank. The PostgreSQL database consists of structured tables that handle customers, accounts, transactions, validation errors, and workflow logs.

---

## 📂 Tables Overview

### 1. 🧍 customers

Stores customer profile data.

| Column       | Type      | Description                        |
|--------------|-----------|------------------------------------|
| `id`         | INTEGER   | Primary key                        |
| `name`       | TEXT      | Full name of the customer          |
| `email`      | TEXT      | Email address (optional)           |
| `created_at` | TIMESTAMP | Customer registration timestamp    |

---

### 2. 🏦 accounts

Stores account data, each linked to a customer.

| Column        | Type      | Description                          |
|---------------|-----------|--------------------------------------|
| `account_id`  | TEXT      | Primary key (e.g. IBAN)              |
| `customer_id` | INTEGER   | Foreign key → `customers(id)`        |
| `currency`    | TEXT      | Account currency (e.g. SEK, EUR)     |
| `created_at`  | TIMESTAMP | Account creation timestamp           |

---

### 3. 💸 transactions

Stores validated financial transactions between two accounts.

| Column                  | Type      | Description                                  |
|-------------------------|-----------|----------------------------------------------|
| `transaction_id`        | INTEGER   | Primary key                                  |
| `timestamp`             | TIMESTAMP | When the transaction took place              |
| `amount`                | NUMERIC   | Amount transferred                           |
| `currency`              | TEXT      | Currency of the transaction                  |
| `sender_account`        | TEXT      | Foreign key → `accounts(account_id)`         |
| `receiver_account`      | TEXT      | Foreign key → `accounts(account_id)`         |
| `sender_country`        | TEXT      | Sender's country                             |
| `sender_municipality`   | TEXT      | Sender's municipality                        |
| `receiver_country`      | TEXT      | Receiver's country                           |
| `receiver_municipality` | TEXT      | Receiver's municipality                      |
| `transaction_type`      | TEXT      | e.g., Transfer, Withdrawal, Deposit          |
| `notes`                 | TEXT      | Optional notes or comments                   |

---

### 4. ❌ invalid_transactions

Stores transactions that failed validation or raised security concerns.

| Column         | Type      | Description                                  |
|----------------|-----------|----------------------------------------------|
| `transaction_id` | INTEGER | Unique ID (not enforced FK)                  |
| `raw_data`     | JSON      | Original transaction row from CSV            |
| `error_message`| TEXT      | Description of validation failure            |
| `detected_at`  | TIMESTAMP | When the issue was identified                |

---

### 5. 📜 logs

System and pipeline log entries for transparency and debugging.

| Column     | Type      | Description                             |
|------------|-----------|-----------------------------------------|
| `id`       | INTEGER   | Primary key                             |
| `step`     | TEXT      | Workflow step (e.g., `validation`)      |
| `message`  | TEXT      | Detailed log message or error context   |
| `status`   | TEXT      | Status such as `success`, `failure`     |
| `timestamp`| TIMESTAMP | Time of the logged event                |

---

## 🔄 Relationships Summary

- Each **account** belongs to one **customer**
- Each **transaction** links a **sender** and a **receiver** account
- **Invalid transactions** are isolated from production data
- **Logs** provide an auditable record of processing activity


---

## 🏃 Running the Model

To run your model, use the following command in your terminal:

```bash
python create_all_tables.py
```

---
---

## 📎 Notes

- All timestamps use UTC by default
- Transactions must pass validation before being inserted
- Invalid records are kept for auditing and correction
- The schema is extensible for fraud detection, notifications, and reporting

---
