from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# 🧠 Update your database credentials here
DATABASE_URL = "postgresql://postgres:pg123456@localhost:5432/bank"

Base = declarative_base()

# 🧍 CUSTOMERS
class Customer(Base):
    __tablename__ = 'customers'

    bankAccount = Column(Text, primary_key=True)  # e.g., IBAN or unique string
    personnummer = Column(Text, nullable=False)
    customer = Column(Text, nullable=False)
    address = Column(Text)
    phone = Column(Text)
    
    BankAccount = relationship("Account", back_populates="customer")


# 🏦 ACCOUNTS
class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(String, primary_key=True)  # e.g., IBAN or unique string
    customer_personnummer = Column(Text, ForeignKey('customers.bankAccount'))
    currency = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="accounts")
    sent_transactions = relationship("Transaction", foreign_keys='Transaction.sender_account', back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys='Transaction.receiver_account', back_populates="receiver")


# 💸 TRANSACTIONS
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Text, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)

    sender_account = Column(String, ForeignKey('accounts.account_id'))
    receiver_account = Column(String, ForeignKey('accounts.account_id'))

    sender_country = Column(String)
    sender_municipality = Column(String)
    receiver_country = Column(String)
    receiver_municipality = Column(String)
    transaction_type = Column(String)
    notes = Column(Text)

    sender = relationship("Account", foreign_keys=[sender_account], back_populates="sent_transactions")
    receiver = relationship("Account", foreign_keys=[receiver_account], back_populates="received_transactions")


# ❌ INVALID TRANSACTIONS
class InvalidTransaction(Base):
    __tablename__ = 'invalid_transactions'

    transaction_id = Column(Integer, primary_key=True)
    raw_data = Column(JSON)
    error_message = Column(Text)
    detected_at = Column(DateTime, default=datetime.utcnow)


# 📜 LOGS
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    step = Column(String)  # e.g., 'validation', 'insert', etc.
    message = Column(Text)
    status = Column(String)  # success, failure, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)


# 🚀 CREATE ALL TABLES
def main():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("✅ All tables created successfully in the 'bank' database.")

if __name__ == "__main__":
    main()
