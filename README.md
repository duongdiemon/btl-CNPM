# btl-CNPM
nhom 6
#
import streamlit as st
import hashlib
import json
import os

# Thiết lập trang
st.set_page_config(
    page_title="Hệ Thống Đăng Nhập",
    page_icon="✅",
    layout="wide"
)

# Hàm để mã hóa mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Hàm để lưu dữ liệu người dùng
def save_users():
    with open('users.json', 'w') as f:
        json.dump(st.session_state.users, f)

# Hàm để tải dữ liệu người dùng
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Khởi tạo session state
if 'users' not in st.session_state:
    st.session_state.users = load_users()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def login_page():
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Đăng Nhập")
        with st.form("login_form"):
            username = st.text_input("👤 Tên đăng nhập:")
            password = st.text_input("🔑 Mật khẩu:", type="password")
            submit = st.form_submit_button("Đăng nhập")
            
            if submit:
                if username in st.session_state.users and st.session_state.users[username]['password'] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.success("✅ Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
        st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 📝 Đăng Ký Tài Khoản")
        with st.form("register_form"):
            username = st.text_input("👤 Tên đăng nhập:")
            password = st.text_input("🔑 Mật khẩu:", type="password")
            confirm_password = st.text_input("🔄 Xác nhận mật khẩu:", type="password")
            submit = st.form_submit_button("Đăng ký")
            
            if submit:
                if username in st.session_state.users:
                    st.error("❌ Tên đăng nhập đã tồn tại!")
                elif password != confirm_password:
                    st.error("❌ Mật khẩu xác nhận không khớp!")
                elif len(password) < 6:
                    st.error("❌ Mật khẩu phải có ít nhất 6 ký tự!")
                else:
                    st.session_state.users[username] = {
                        'password': hash_password(password)
                    }
                    save_users()
                    st.success("✅ Đăng ký thành công! Vui lòng đăng nhập.")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>✅ Hệ Thống Đăng Nhập</h1>", unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        with tab1:
            login_page()
        with tab2:
            register_page()
        return

    # Header với thông tin người dùng
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.markdown(f'<p class="welcome-text">👋 Xin chào, {st.session_state.current_user}!</p>', unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

if __name__ == "__main__":
    main()
# Bảo Mật và Sao Lưu
import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import base64
from cryptography.fernet import Fernet
import shutil
import zipfile
from pathlib import Path

# Thiết lập trang
st.set_page_config(
    page_title="Bảo Mật & Sao Lưu Dữ Liệu",
    page_icon="🔒",
    layout="wide"
)

# Khởi tạo session state
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Hàm mã hóa dữ liệu
def encrypt_data(data):
    if not st.session_state.encryption_key:
        st.session_state.encryption_key = Fernet.generate_key()
    f = Fernet(st.session_state.encryption_key)
    return f.encrypt(json.dumps(data).encode()).decode()

# Hàm giải mã dữ liệu
def decrypt_data(encrypted_data):
    if not st.session_state.encryption_key:
        return None
    f = Fernet(st.session_state.encryption_key)
    try:
        return json.loads(f.decrypt(encrypted_data.encode()).decode())
    except:
        return None

# Hàm tạo mật khẩu hash
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Hàm xác thực người dùng
def authenticate_user(username, password):
    if os.path.exists('user_credentials.json'):
        with open('user_credentials.json', 'r') as f:
            credentials = json.load(f)
            if username in credentials and credentials[username]['password'] == hash_password(password):
                st.session_state.is_authenticated = True
                st.session_state.encryption_key = credentials[username]['encryption_key'].encode()
                return True
    return False

# Hàm đăng ký người dùng mới
def register_user(username, password):
    if os.path.exists('user_credentials.json'):
        with open('user_credentials.json', 'r') as f:
            credentials = json.load(f)
    else:
        credentials = {}
    
    if username in credentials:
        return False, "Tên đăng nhập đã tồn tại!"
    
    encryption_key = Fernet.generate_key()
    credentials[username] = {
        'password': hash_password(password),
        'encryption_key': encryption_key.decode()
    }
    
    with open('user_credentials.json', 'w') as f:
        json.dump(credentials, f)
    
    return True, "Đăng ký thành công!"

# Hàm sao lưu dữ liệu
def backup_data():
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"backup_{timestamp}.zip"
    
    with zipfile.ZipFile(backup_file, 'w') as zipf:
        if os.path.exists('user_credentials.json'):
            zipf.write('user_credentials.json')
        if os.path.exists('encrypted_data.json'):
            zipf.write('encrypted_data.json')
    
    return backup_file

# Hàm khôi phục dữ liệu
def restore_data(backup_file):
    try:
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall()
        return True, "Khôi phục dữ liệu thành công!"
    except Exception as e:
        return False, f"Lỗi khi khôi phục: {str(e)}"

def login_page():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🔒 Đăng Nhập Hệ Thống</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập:")
            password = st.text_input("Mật khẩu:", type="password")
            submit = st.form_submit_button("Đăng nhập")
            
            if submit:
                if authenticate_user(username, password):
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng!")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Tên đăng nhập mới:")
            new_password = st.text_input("Mật khẩu mới:", type="password")
            confirm_password = st.text_input("Xác nhận mật khẩu:", type="password")
            submit = st.form_submit_button("Đăng ký")
            
            if submit:
                if new_password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp!")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

def main_page():
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🔒 Bảo Mật & Sao Lưu Dữ Liệu</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Quản lý dữ liệu", "Sao lưu", "Khôi phục"])
    
    with tab1:
        st.markdown("### 📝 Quản Lý Dữ Liệu")
        with st.form("data_form"):
            data_type = st.selectbox("Loại dữ liệu:", ["Thông tin cá nhân", "Tài liệu quan trọng", "Mật khẩu"])
            content = st.text_area("Nội dung:")
            submit = st.form_submit_button("Lưu")
            
            if submit:
                if not st.session_state.user_data:
                    st.session_state.user_data = {}
                
                st.session_state.user_data[data_type] = content
                encrypted_data = encrypt_data(st.session_state.user_data)
                
                with open('encrypted_data.json', 'w') as f:
                    json.dump({'data': encrypted_data}, f)
                
                st.success("Đã lưu dữ liệu thành công!")
        
        if st.session_state.user_data:
            st.markdown("### 📋 Dữ Liệu Đã Lưu")
            for data_type, content in st.session_state.user_data.items():
                with st.expander(data_type):
                    st.text(content)
    
    with tab2:
        st.markdown("### 💾 Sao Lưu Dữ Liệu")
        if st.button("Tạo bản sao lưu"):
            backup_file = backup_data()
            st.success(f"Đã tạo bản sao lưu: {backup_file.name}")
    
    with tab3:
        st.markdown("### 🔄 Khôi Phục Dữ Liệu")
        backup_dir = Path("backups")
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("backup_*.zip"))
            if backup_files:
                selected_backup = st.selectbox(
                    "Chọn bản sao lưu:",
                    backup_files,
                    format_func=lambda x: x.name
                )
                if st.button("Khôi phục"):
                    success, message = restore_data(selected_backup)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.info("Chưa có bản sao lưu nào!")
        else:
            st.info("Chưa có thư mục sao lưu!")

def main():
    if not st.session_state.is_authenticated:
        login_page()
    else:
        main_page()
        
        if st.sidebar.button("Đăng xuất"):
            st.session_state.is_authenticated = False
            st.session_state.encryption_key = None
            st.session_state.user_data = {}
            st.rerun()

if __name__ == "__main__":
    main()
