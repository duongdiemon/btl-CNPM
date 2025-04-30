from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    INCOME = "Thu nhập"
    EXPENSE = "Chi tiêu"
    LOAN = "Khoản vay"
    DEBT = "Khoản nợ"

class Transaction:
    def __init__(self, amount, description, date, category, transaction_type, budget_id=None, loan_id=None):
        self.amount = amount
        self.description = description
        self.date = date
        self.category = category
        self.transaction_type = transaction_type
        self.budget_id = budget_id
        self.loan_id = loan_id

    def to_dict(self):
        return {
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
            "category": self.category,
            "transaction_type": self.transaction_type.value,
            "budget_id": self.budget_id,
            "loan_id": self.loan_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            amount=data["amount"],
            description=data["description"],
            date=data["date"],
            category=data["category"],
            transaction_type=TransactionType(data["transaction_type"]),
            budget_id=data.get("budget_id"),
            loan_id=data.get("loan_id")
        ) 