import streamlit as st
from models.auth import AuthManager

def register_page():
    st.title("Đăng ký tài khoản")
    
    with st.form("register_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password")
        
        submitted = st.form_submit_button("Đăng ký")
        
        if submitted:
            if not username or not password or not confirm_password:
                st.error("Vui lòng điền đầy đủ thông tin!")
            elif password != confirm_password:
                st.error("Mật khẩu xác nhận không khớp!")
            else:
                auth_manager = AuthManager()
                success, message = auth_manager.register(username, password)
                if success:
                    st.success("🎉 Đăng ký tài khoản thành công! Vui lòng đăng nhập để tiếp tục.")
                    st.session_state.show_register = False
                    st.session_state.show_login = True
                    st.rerun()
                else:
                    st.error(message)
    
    if st.button("Quay lại đăng nhập"):
        st.session_state.show_register = False
        st.session_state.show_login = True
        st.rerun() 