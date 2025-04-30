import streamlit as st
from models.auth import AuthManager

def login_page():
    st.title("Đăng nhập")
    
    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        
        submitted = st.form_submit_button("Đăng nhập")
        
        if submitted:
            if not username or not password:
                st.error("Vui lòng điền đầy đủ thông tin!")
            else:
                auth_manager = AuthManager()
                success, message = auth_manager.login(username, password)
                if success:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = auth_manager.get_user(username)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    if st.button("Đăng ký tài khoản mới"):
        st.session_state.show_register = True
        st.session_state.show_login = False
        st.rerun() 