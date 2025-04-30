from datetime import datetime

class Loan:
    def __init__(self, name, amount, interest_rate, start_date, end_date, loan_type="Khoản vay"):
        self.name = name
        self.amount = amount
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.end_date = end_date
        self.loan_type = loan_type
        self.paid = 0
        self.payments = []

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "loan_type": self.loan_type,
            "paid": self.paid,
            "payments": self.payments
        }

    @classmethod
    def from_dict(cls, data):
        loan = cls(
            name=data["name"],
            amount=data["amount"],
            interest_rate=data["interest_rate"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            loan_type=data.get("loan_type", "Khoản vay")
        )
        loan.paid = data.get("paid", 0)
        loan.payments = data.get("payments", [])
        return loan

    def add_payment(self, amount, date):
        self.payments.append({
            "amount": amount,
            "date": date
        })
        self.paid += amount

    def get_remaining(self):
        return self.amount - self.paid

    def get_interest_amount(self):
        return self.amount * (self.interest_rate / 100)

    def get_total_amount(self):
        return self.amount + self.get_interest_amount() 