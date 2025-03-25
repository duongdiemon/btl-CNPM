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
