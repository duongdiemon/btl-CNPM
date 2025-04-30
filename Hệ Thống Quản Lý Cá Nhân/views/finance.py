import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from models.transaction import Transaction, TransactionType
from models.budget import Budget
from models.loan import Loan

def finance_page():
    st.title("💰 Quản lý tài chính")
    
    # Khởi tạo dữ liệu nếu chưa có
    if not hasattr(st.session_state.current_user, 'transactions'):
        st.session_state.current_user.transactions = []
    if not hasattr(st.session_state.current_user, 'budgets'):
        st.session_state.current_user.budgets = []
    if not hasattr(st.session_state.current_user, 'loans'):
        st.session_state.current_user.loans = []
    
    # Tab điều hướng
    tab1, tab2, tab3 = st.tabs(["📊 Thu chi", "📋 Ngân sách", "💳 Khoản vay/nợ"])
    
    with tab1:
        st.subheader("📊 Theo dõi thu chi")
        
        # Form thêm giao dịch mới
        with st.expander("➕ Thêm giao dịch mới", expanded=True):
            with st.form("add_transaction_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    amount = st.number_input("Số tiền", min_value=0, step=1000)
                    transaction_type = st.selectbox(
                        "Loại giao dịch",
                        ["Thu nhập", "Chi tiêu", "Khoản vay", "Khoản nợ"]
                    )
                with col2:
                    date = st.date_input("Ngày", value=datetime.now().date())
                    category = st.text_input("Danh mục")
                
                description = st.text_area("Mô tả")
                
                submit_button = st.form_submit_button("Thêm")
                
                if submit_button:
                    if amount > 0 and category:
                        try:
                            # Chuyển đổi loại giao dịch thành enum
                            type_enum = {
                                "Thu nhập": TransactionType.INCOME,
                                "Chi tiêu": TransactionType.EXPENSE,
                                "Khoản vay": TransactionType.LOAN,
                                "Khoản nợ": TransactionType.DEBT
                            }[transaction_type]
                            
                            new_transaction = Transaction(
                                amount=amount,
                                description=description,
                                date=date,
                                category=category,
                                transaction_type=type_enum
                            )
                            
                            # Thêm giao dịch vào danh sách
                            if not hasattr(st.session_state.current_user, 'transactions'):
                                st.session_state.current_user.transactions = []
                            st.session_state.current_user.transactions.append(new_transaction.to_dict())
                            
                            st.success("✅ Đã thêm giao dịch mới!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Lỗi khi thêm giao dịch: {str(e)}")
                    else:
                        st.error("❌ Vui lòng điền đầy đủ thông tin!")
        
        # Hiển thị bảng giao dịch
        if st.session_state.current_user.transactions:
            # Chuyển đổi dữ liệu thành DataFrame
            transactions = [Transaction.from_dict(t) for t in st.session_state.current_user.transactions]
            df = pd.DataFrame([{
                'Ngày': t.date,
                'Loại': t.transaction_type.value,
                'Danh mục': t.category,
                'Số tiền': t.amount,
                'Mô tả': t.description
            } for t in transactions])
            
            # Sắp xếp theo ngày
            df = df.sort_values('Ngày', ascending=False)
            
            # Hiển thị bảng
            st.dataframe(df, use_container_width=True)
            
            # Thống kê
            col1, col2, col3 = st.columns(3)
            with col1:
                total_income = df[df['Loại'] == TransactionType.INCOME.value]['Số tiền'].sum()
                st.metric("Tổng thu", f"{total_income:,.0f} VNĐ")
            with col2:
                total_expense = df[df['Loại'] == TransactionType.EXPENSE.value]['Số tiền'].sum()
                st.metric("Tổng chi", f"{total_expense:,.0f} VNĐ")
            with col3:
                balance = total_income - total_expense
                st.metric("Số dư", f"{balance:,.0f} VNĐ")
            
            # Biểu đồ phân bố theo danh mục
            st.subheader("📈 Phân bố chi tiêu theo danh mục")
            category_sum = df[df['Loại'] == TransactionType.EXPENSE.value].groupby('Danh mục')['Số tiền'].sum().reset_index()
            st.bar_chart(category_sum, x='Danh mục', y='Số tiền')
        else:
            st.info("📝 Chưa có giao dịch nào!")
    
    with tab2:
        st.subheader("📋 Quản lý ngân sách")
        
        # Form thêm ngân sách mới
        with st.expander("➕ Thêm ngân sách mới", expanded=True):
            with st.form("add_budget_form", clear_on_submit=True):
                name = st.text_input("Tên ngân sách")
                amount = st.number_input("Số tiền", min_value=0)
                category = st.text_input("Danh mục")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Ngày bắt đầu", value=datetime.now().date())
                with col2:
                    end_date = st.date_input("Ngày kết thúc", value=datetime.now().date() + timedelta(days=30))
                
                submit_button = st.form_submit_button("Thêm")
                
                if submit_button:
                    if name and amount > 0 and start_date < end_date:
                        new_budget = Budget(
                            name=name,
                            amount=amount,
                            start_date=start_date,
                            end_date=end_date,
                            category=category
                        )
                        st.session_state.current_user.budgets.append(new_budget.to_dict())
                        st.success("✅ Đã thêm ngân sách mới!")
                        st.rerun()
        
        # Hiển thị ngân sách
        if st.session_state.current_user.budgets:
            budgets = [Budget.from_dict(b) for b in st.session_state.current_user.budgets]
            
            # Cập nhật số tiền đã chi cho mỗi ngân sách
            if st.session_state.current_user.transactions:
                transactions = [Transaction.from_dict(t) for t in st.session_state.current_user.transactions]
                for budget in budgets:
                    # Tính tổng chi tiêu trong danh mục của ngân sách
                    category_expenses = sum(
                        t.amount for t in transactions 
                        if t.transaction_type == TransactionType.EXPENSE 
                        and t.category == budget.category
                        and budget.start_date <= t.date <= budget.end_date
                    )
                    budget.spent = category_expenses
            
            # Hiển thị từng ngân sách
            for budget in budgets:
                with st.expander(f"📋 {budget.name} - {budget.amount:,.0f} VNĐ"):
                    st.write(f"**Danh mục:** {budget.category}")
                    st.write(f"**Thời gian:** {budget.start_date} - {budget.end_date}")
                    st.write(f"**Đã chi:** {budget.spent:,.0f} VNĐ")
                    st.write(f"**Còn lại:** {budget.get_remaining():,.0f} VNĐ")
                    
                    # Hiển thị thanh tiến độ
                    progress = budget.get_percentage_spent() / 100
                    st.progress(progress)
                    
                    # Hiển thị cảnh báo nếu chi tiêu vượt quá ngân sách
                    if progress > 1:
                        st.error("⚠️ Chi tiêu đã vượt quá ngân sách!")
                    elif progress > 0.8:
                        st.warning("⚠️ Chi tiêu đã gần đạt giới hạn ngân sách!")
        else:
            st.info("📝 Chưa có ngân sách nào!")
    
    with tab3:
        st.subheader("💳 Quản lý khoản vay/nợ")
        
        # Form thêm khoản vay/nợ mới
        with st.expander("➕ Thêm khoản vay/nợ mới", expanded=True):
            with st.form("add_loan_form", clear_on_submit=True):
                name = st.text_input("Tên khoản vay/nợ")
                amount = st.number_input("Số tiền", min_value=0)
                interest_rate = st.number_input("Lãi suất (%)", min_value=0.0, max_value=100.0)
                loan_type = st.selectbox("Loại", ["Khoản vay", "Khoản nợ"])
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Ngày bắt đầu", value=datetime.now().date())
                with col2:
                    end_date = st.date_input("Ngày kết thúc", value=datetime.now().date() + timedelta(days=30))
                
                submit_button = st.form_submit_button("Thêm")
                
                if submit_button:
                    if name and amount > 0 and start_date < end_date:
                        new_loan = Loan(
                            name=name,
                            amount=amount,
                            interest_rate=interest_rate,
                            start_date=start_date,
                            end_date=end_date,
                            loan_type=loan_type
                        )
                        st.session_state.current_user.loans.append(new_loan.to_dict())
                        st.success("✅ Đã thêm khoản vay/nợ mới!")
                        st.rerun()
        
        # Hiển thị khoản vay/nợ
        if st.session_state.current_user.loans:
            for loan_data in st.session_state.current_user.loans:
                loan = Loan.from_dict(loan_data)
                with st.expander(f"💳 {loan.name} - {loan.amount:,.0f} VNĐ"):
                    st.write(f"**Loại:** {loan.loan_type}")
                    st.write(f"**Lãi suất:** {loan.interest_rate}%")
                    st.write(f"**Thời gian:** {loan.start_date} - {loan.end_date}")
                    st.write(f"**Đã trả:** {loan.paid:,.0f} VNĐ")
                    st.write(f"**Còn lại:** {loan.get_remaining():,.0f} VNĐ")
                    st.write(f"**Lãi:** {loan.get_interest_amount():,.0f} VNĐ")
                    st.write(f"**Tổng cộng:** {loan.get_total_amount():,.0f} VNĐ")
                    
                    # Form thêm khoản thanh toán
                    with st.form(f"add_payment_{loan.name}"):
                        payment_amount = st.number_input("Số tiền thanh toán", min_value=0)
                        payment_date = st.date_input("Ngày thanh toán", value=datetime.now().date())
                        
                        submit_button = st.form_submit_button("Thêm thanh toán")
                        if submit_button and payment_amount > 0:
                            loan.add_payment(payment_amount, payment_date)
                            st.session_state.current_user.loans = [l.to_dict() for l in [Loan.from_dict(l) for l in st.session_state.current_user.loans]]
                            st.success("✅ Đã thêm thanh toán!")
                            st.rerun()
        else:
            st.info("📝 Chưa có khoản vay/nợ nào!") 