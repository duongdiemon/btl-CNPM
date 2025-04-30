import streamlit as st
from models.auth import AuthManager

class AuthController:
    def __init__(self):
        self.auth_manager = AuthManager()

    def handle_login(self, username, password):
        """Xử lý đăng nhập"""
        if not username or not password:
            return False, "Vui lòng điền đầy đủ thông tin!"
        
        success, message = self.auth_manager.login(username, password)
        if success:
            st.session_state.is_logged_in = True
            st.session_state.current_user = self.auth_manager.get_user(username)
            return True, message
        return False, message

    def handle_register(self, username, password):
        """Xử lý đăng ký"""
        if not username or not password:
            return False, "Vui lòng điền đầy đủ thông tin!"
        
        success, message = self.auth_manager.register(username, password)
        if success:
            st.session_state.show_register = False
            st.session_state.show_login = True
        return success, message

    def handle_logout(self):
        """Xử lý đăng xuất"""
        st.session_state.is_logged_in = False
        st.session_state.current_user = None
        st.session_state.show_login = True 