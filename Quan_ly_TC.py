import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Thiết lập trang
st.set_page_config(
    page_title="Quản Lý Tài Chính",
    page_icon="💰",
    layout="wide"
)

# Hàm để lưu dữ liệu
def save_data():
    with open('financial_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'transactions': st.session_state.transactions,
            'categories': st.session_state.categories
        }, f, ensure_ascii=False)

# Hàm để tải dữ liệu
def load_data():
    if os.path.exists('financial_data.json'):
        try:
            with open('financial_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('transactions', []), data.get('categories', {
                    'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
                    'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Hóa đơn', 'Khác']
                })
        except:
            return [], {
                'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
                'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Hóa đơn', 'Khác']
            }
    return [], {
        'income': ['Lương', 'Thưởng', 'Đầu tư', 'Khác'],
        'expense': ['Ăn uống', 'Di chuyển', 'Mua sắm', 'Hóa đơn', 'Khác']
    }

# Khởi tạo session state
if 'transactions' not in st.session_state:
    st.session_state.transactions, st.session_state.categories = load_data()

def add_transaction():
    with st.form("add_transaction_form"):
        st.markdown("### 📝 Thêm Giao Dịch Mới")
        
        col1, col2 = st.columns(2)
        with col1:
            transaction_type = st.radio("Loại giao dịch:", ["Thu", "Chi"])
            amount = st.number_input("Số tiền:", min_value=0.0, step=1000.0)
            category = st.selectbox(
                "Danh mục:",
                st.session_state.categories['income' if transaction_type == "Thu" else 'expense']
            )
        
        with col2:
            date = st.date_input("Ngày:", value=datetime.now().date())
            description = st.text_input("Mô tả:")
            payment_method = st.selectbox(
                "Phương thức thanh toán:",
                ["Tiền mặt", "Thẻ tín dụng", "Chuyển khoản", "Ví điện tử", "Khác"]
            )
        
        submit = st.form_submit_button("Thêm giao dịch")
        
        if submit:
            if amount <= 0:
                st.error("Vui lòng nhập số tiền hợp lệ!")
                return
                
            new_transaction = {
                "id": len(st.session_state.transactions),
                "type": transaction_type,
                "amount": amount,
                "category": category,
                "date": date.strftime("%Y-%m-%d"),
                "description": description,
                "payment_method": payment_method
            }
            st.session_state.transactions.append(new_transaction)
            save_data()
            st.success("✅ Đã thêm giao dịch mới!")

def view_transactions():
    st.markdown("### 📋 Danh Sách Giao Dịch")
    
    if not st.session_state.transactions:
        st.info("Chưa có giao dịch nào. Hãy thêm giao dịch mới!")
        return
    
    # Tạo DataFrame từ danh sách giao dịch
    df = pd.DataFrame(st.session_state.transactions)
    
    # Thêm bộ lọc
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Lọc theo loại:", ["Tất cả", "Thu", "Chi"])
    with col2:
        filter_category = st.selectbox("Lọc theo danh mục:", ["Tất cả"] + 
                                     list(set([t['category'] for t in st.session_state.transactions])))
    with col3:
        filter_date = st.date_input("Lọc theo ngày:", value=datetime.now().date())
    
    # Áp dụng bộ lọc
    if filter_type != "Tất cả":
        df = df[df['type'] == filter_type]
    if filter_category != "Tất cả":
        df = df[df['category'] == filter_category]
    df = df[df['date'] == filter_date.strftime("%Y-%m-%d")]
    
    # Hiển thị bảng
    st.dataframe(df)

def financial_report():
    st.markdown("### 📊 Báo Cáo Tài Chính")
    
    if not st.session_state.transactions:
        st.info("Chưa có dữ liệu để tạo báo cáo!")
        return
    
    # Tạo DataFrame
    df = pd.DataFrame(st.session_state.transactions)
    
    # Chọn khoảng thời gian
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Từ ngày:", value=datetime.now().date() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Đến ngày:", value=datetime.now().date())
    
    # Lọc theo khoảng thời gian
    df['date'] = pd.to_datetime(df['date'])
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    df = df[mask]
    
    # Tính tổng thu chi
    total_income = df[df['type'] == 'Thu']['amount'].sum()
    total_expense = df[df['type'] == 'Chi']['amount'].sum()
    balance = total_income - total_expense
    
    # Hiển thị tổng quan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng Thu", f"{total_income:,.0f}đ")
    with col2:
        st.metric("Tổng Chi", f"{total_expense:,.0f}đ")
    with col3:
        st.metric("Số Dư", f"{balance:,.0f}đ")
    
    # Biểu đồ thu chi theo danh mục
    st.markdown("#### 📈 Thu Chi Theo Danh Mục")
    
    # Thu
    income_by_category = df[df['type'] == 'Thu'].groupby('category')['amount'].sum().reset_index()
    expense_by_category = df[df['type'] == 'Chi'].groupby('category')['amount'].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_income = px.pie(income_by_category, values='amount', names='category', title='Phân Bố Thu')
        st.plotly_chart(fig_income, use_container_width=True)
    
    with col2:
        fig_expense = px.pie(expense_by_category, values='amount', names='category', title='Phân Bố Chi')
        st.plotly_chart(fig_expense, use_container_width=True)
    
    # Biểu đồ thu chi theo thời gian
    st.markdown("#### 📅 Thu Chi Theo Thời Gian")
    daily_data = df.groupby(['date', 'type'])['amount'].sum().reset_index()
    
    fig_timeline = go.Figure()
    for type_ in ['Thu', 'Chi']:
        type_data = daily_data[daily_data['type'] == type_]
        fig_timeline.add_trace(go.Scatter(
            x=type_data['date'],
            y=type_data['amount'],
            name=type_,
            mode='lines+markers'
        ))
    
    fig_timeline.update_layout(title='Thu Chi Theo Thời Gian')
    st.plotly_chart(fig_timeline, use_container_width=True)

def manage_categories():
    st.markdown("### ⚙️ Quản Lý Danh Mục")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Danh Mục Thu")
        for i, category in enumerate(st.session_state.categories['income']):
            col1a, col1b = st.columns([3, 1])
            with col1a:
                st.text_input(f"Danh mục thu {i+1}:", value=category, key=f"income_cat_{i}")
            with col1b:
                if st.button("Xóa", key=f"del_income_{i}"):
                    st.session_state.categories['income'].pop(i)
                    save_data()
                    st.rerun()
    
    with col2:
        st.markdown("#### Danh Mục Chi")
        for i, category in enumerate(st.session_state.categories['expense']):
            col2a, col2b = st.columns([3, 1])
            with col2a:
                st.text_input(f"Danh mục chi {i+1}:", value=category, key=f"expense_cat_{i}")
            with col2b:
                if st.button("Xóa", key=f"del_expense_{i}"):
                    st.session_state.categories['expense'].pop(i)
                    save_data()
                    st.rerun()
    
    # Thêm danh mục mới
    st.markdown("#### Thêm Danh Mục Mới")
    col1, col2 = st.columns(2)
    with col1:
        new_income = st.text_input("Thêm danh mục thu mới:")
        if st.button("Thêm", key="add_income"):
            if new_income and new_income not in st.session_state.categories['income']:
                st.session_state.categories['income'].append(new_income)
                save_data()
                st.rerun()
    
    with col2:
        new_expense = st.text_input("Thêm danh mục chi mới:")
        if st.button("Thêm", key="add_expense"):
            if new_expense and new_expense not in st.session_state.categories['expense']:
                st.session_state.categories['expense'].append(new_expense)
                save_data()
                st.rerun()

def main():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>💰 Quản Lý Tài Chính</h1>", unsafe_allow_html=True)
    
    # Tạo tabs cho các chức năng
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Thêm giao dịch", "📋 Danh sách", "📊 Báo cáo", "⚙️ Quản lý danh mục"])
    
    with tab1:
        add_transaction()
    
    with tab2:
        view_transactions()
    
    with tab3:
        financial_report()
    
    with tab4:
        manage_categories()

if __name__ == "__main__":
    main()