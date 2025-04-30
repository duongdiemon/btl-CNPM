import streamlit as st
import os
from datetime import datetime
from typing import Optional
from LM.models.user_profile import UserProfile

def save_avatar(avatar_file) -> Optional[str]:
    """Lưu avatar và trả về đường dẫn"""
    try:
        if not os.path.exists("avatars"):
            os.makedirs("avatars")
            
        file_path = os.path.join("avatars", f"{st.session_state.username}_{avatar_file.name}")
        with open(file_path, "wb") as f:
            f.write(avatar_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Lỗi khi lưu avatar: {str(e)}")
        return None

def profile_page():
    st.title("Thông tin cá nhân")
    
    # Khởi tạo profile nếu chưa có
    if "profile" not in st.session_state:
        st.session_state.profile = UserProfile(username=st.session_state.username)
    
    # Hiển thị thông tin hiện tại
    st.subheader("Thông tin hiện tại")
    profile = st.session_state.profile
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if profile.avatar and os.path.exists(profile.avatar):
            st.image(profile.avatar, width=200)
        else:
            st.info("Chưa có avatar")
    
    with col2:
        st.write(f"**Tên đầy đủ:** {profile.full_name or 'Chưa cập nhật'}")
        st.write(f"**Email:** {profile.email or 'Chưa cập nhật'}")
        st.write(f"**Số điện thoại:** {profile.phone or 'Chưa cập nhật'}")
        st.write(f"**Địa chỉ:** {profile.address or 'Chưa cập nhật'}")
        st.write(f"**Ngày sinh:** {profile.birth_date.strftime('%d/%m/%Y') if profile.birth_date else 'Chưa cập nhật'}")
        st.write(f"**Giới tính:** {profile.gender or 'Chưa cập nhật'}")
    
    # Form chỉnh sửa thông tin
    st.subheader("Chỉnh sửa thông tin")
    with st.form("profile_form"):
        new_full_name = st.text_input("Họ và tên", value=profile.full_name or "")
        new_email = st.text_input("Email", value=profile.email or "")
        new_phone = st.text_input("Số điện thoại", value=profile.phone or "")
        new_address = st.text_area("Địa chỉ", value=profile.address or "")
        new_birth_date = st.date_input("Ngày sinh", value=profile.birth_date or datetime.now())
        new_gender = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"], 
                                index=["Nam", "Nữ", "Khác"].index(profile.gender) if profile.gender else 0)
        
        new_avatar = st.file_uploader("Avatar", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("Cập nhật")
        
        if submitted:
            try:
                # Cập nhật thông tin
                profile.update(
                    full_name=new_full_name,
                    email=new_email,
                    phone=new_phone,
                    address=new_address,
                    birth_date=new_birth_date,
                    gender=new_gender
                )
                
                # Xử lý avatar
                if new_avatar:
                    avatar_path = save_avatar(new_avatar)
                    if avatar_path:
                        profile.update(avatar=avatar_path)
                
                # Kiểm tra tính hợp lệ
                if not profile.validate():
                    st.error("Thông tin không hợp lệ. Vui lòng kiểm tra lại.")
                    return
                
                # Lưu vào session
                st.session_state.profile = profile
                st.success("Cập nhật thông tin thành công!")
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}") 