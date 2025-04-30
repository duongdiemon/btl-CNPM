from datetime import datetime

class Budget:
    def __init__(self, name, amount, start_date, end_date, category=None):
        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.category = category
        self.spent = 0

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "category": self.category,
            "spent": self.spent
        }

    @classmethod
    def from_dict(cls, data):
        budget = cls(
            name=data["name"],
            amount=data["amount"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            category=data.get("category")
        )
        budget.spent = data.get("spent", 0)
        return budget

    def update_spent(self, amount):
        self.spent += amount

    def get_remaining(self):
        return self.amount - self.spent

    def get_percentage_spent(self):
        return (self.spent / self.amount) * 100 if self.amount > 0 else 0 