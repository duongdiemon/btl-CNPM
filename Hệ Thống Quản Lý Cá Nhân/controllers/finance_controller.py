import streamlit as st
from models.transaction import Transaction
from models.budget import Budget
from models.loan import Loan

class FinanceController:
    def __init__(self):
        self.current_user = st.session_state.current_user

    def add_transaction(self, amount, category, description, date):
        """Thêm giao dịch mới"""
        transaction = Transaction(amount, category, description, date)
        self.current_user.transactions.append(transaction)
        return True, "Thêm giao dịch thành công"

    def create_budget(self, category, amount, period):
        """Tạo ngân sách mới"""
        budget = Budget(category, amount, period)
        self.current_user.budgets.append(budget)
        return True, "Tạo ngân sách thành công"

    def add_loan(self, amount, interest_rate, term, description):
        """Thêm khoản vay mới"""
        loan = Loan(amount, interest_rate, term, description)
        self.current_user.loans.append(loan)
        return True, "Thêm khoản vay thành công"

    def get_transactions(self):
        """Lấy danh sách giao dịch"""
        return self.current_user.transactions

    def get_budgets(self):
        """Lấy danh sách ngân sách"""
        return self.current_user.budgets

    def get_loans(self):
        """Lấy danh sách khoản vay"""
        return self.current_user.loans 