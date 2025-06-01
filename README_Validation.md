## 🧪 Data Validation with Great Expectations

This project includes a validation pipeline using **[Great Expectations](https://greatexpectations.io/)** to ensure the quality of transaction and customer data before it is processed into the system.

### 📦 Dependencies

Install Great Expectations (if not already installed):

```bash
pip install great_expectations
```

Other required libraries:
```bash
pip install pandas
```

---

### 🧰 What the Script Does

The validation script:

1. **Loads transaction and customer data** from CSV files located in the `./data` folder.
2. **Cleans the data** by removing duplicates and critical null values.
3. **Creates a validation context** using Great Expectations.
4. **Adds expectations** for data quality, such as:
   - Required columns must exist
   - No nulls in critical columns
   - Unique `transaction_id`s
   - Valid amount ranges
   - Valid currencies and transaction types
   - Proper timestamp format
5. **Validates the dataset** and prints results.

---

### 🧪 Example Validations

| Check | Rule |
|-------|------|
| Column existence | `transaction_id`, `timestamp`, `amount`, etc. must exist |
| No nulls | Key columns must not be null |
| Unique IDs | `transaction_id` must be unique |
| Range check | `amount` must be between 0.01 and 100,000 |
| Format check | `timestamp` must match `%Y-%m-%d %H:%M:%S` |
| Allowed values | `currency` should be `SEK`, type should be `incoming` or `outgoing` |

---

### ▶️ How to Run

1. Ensure the CSV files are available in the `/data` folder.
2. Run the script:

```bash
python validate_transactions.ipynb
```
