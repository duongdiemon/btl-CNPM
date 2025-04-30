import streamlit as st
from models.user_profile import UserProfile

class ProfileController:
    def __init__(self):
        self.current_user = st.session_state.current_user

    def update_profile(self, name, phone, address, avatar=None):
        """Cập nhật thông tin cá nhân"""
        self.current_user.personal_info['name'] = name
        self.current_user.personal_info['phone'] = phone
        self.current_user.personal_info['address'] = address
        
        if avatar:
            self.current_user.avatar = avatar
            
        return True, "Cập nhật thông tin thành công"

    def get_profile(self):
        """Lấy thông tin cá nhân"""
        return self.current_user.personal_info

    def change_password(self, old_password, new_password):
        """Thay đổi mật khẩu"""
        if self.current_user.password != old_password:
            return False, "Mật khẩu cũ không đúng"
        
        self.current_user.password = new_password
        return True, "Thay đổi mật khẩu thành công" 