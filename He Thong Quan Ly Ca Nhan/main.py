import streamlit as st
from views.login import login_page
from views.register import register_page
from views.tasks import tasks_page
from views.time_management import time_management_page
from views.finance import finance_page
from views.notes import notes_page
from views.backup import backup_page
from LM.views.profile import profile_page

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý Cá Nhân",
    page_icon="��",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .css-1v0mbdj {
        border-radius: 10px;
    }
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        padding: 20px;
    }
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 500px;
        text-align: center;
    }
    .login-logo {
        margin-bottom: 30px;
    }
    .login-title {
        font-size: 2em;
        margin-bottom: 20px;
        color: #333;
    }
    .login-subtitle {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo session state
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = True
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Quản lý công việc"
if 'username' not in st.session_state:
    st.session_state.username = "user1"

def main():
    if not st.session_state.is_logged_in:
        if st.session_state.show_register:
            register_page()
        else:
            login_page()
    else:
        # Hiển thị lời chào
        st.title(f"Xin chào, {st.session_state.current_user.username}!")
        
        # Menu chính
        menu = st.sidebar.selectbox(
            "Chọn chức năng",
            ["Quản lý công việc", "Quản lý thời gian", "Quản lý tài chính", "📝 Ghi chú", "📦 Sao lưu", "👤 Thông tin cá nhân"]
        )
        
        # Xử lý các lựa chọn menu
        if menu == "Quản lý công việc":
            tasks_page()
        elif menu == "Quản lý thời gian":
            time_management_page()
        elif menu == "Quản lý tài chính":
            finance_page()
        elif menu == "📝 Ghi chú":
            notes_page()
        elif menu == "📦 Sao lưu":
            backup_page()
        elif menu == "👤 Thông tin cá nhân":
            profile_page()
        
        # Nút đăng xuất
        if st.sidebar.button("🚪 Đăng xuất"):
            st.session_state.is_logged_in = False
            st.session_state.current_user = None
            st.session_state.show_login = True
            st.rerun()

if __name__ == "__main__":
    main() 