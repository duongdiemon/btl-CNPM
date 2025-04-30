import streamlit as st
from utils.backup import backup_data, restore_data, get_backup_files
import os

def backup_page():
    st.title("📦 Sao lưu & Khôi phục")
    
    # Tab điều hướng
    tab1, tab2 = st.tabs(["Sao lưu dữ liệu", "Khôi phục dữ liệu"])
    
    with tab1:
        st.subheader("Sao lưu dữ liệu")
        st.write("Tạo bản sao lưu dữ liệu hiện tại của bạn.")
        
        if st.button("Tạo bản sao lưu", use_container_width=True):
            # Lấy dữ liệu người dùng hiện tại
            user_data = {
                "username": st.session_state.current_user.username,
                "notes": st.session_state.current_user.notes,
                "tasks": st.session_state.current_user.tasks,
                "events": st.session_state.current_user.events,
                "finance": st.session_state.current_user.finance
            }
            
            # Tạo bản sao lưu
            backup_file = backup_data(user_data)
            if backup_file:
                st.success(f"✅ Đã tạo bản sao lưu thành công: {os.path.basename(backup_file)}")
            else:
                st.error("❌ Không thể tạo bản sao lưu!")
        
        # Hiển thị danh sách các bản sao lưu
        st.subheader("Danh sách bản sao lưu")
        backup_files = get_backup_files()
        
        if backup_files:
            for backup in backup_files:
                with st.expander(f"📦 {backup['name']} - {backup['created_at'].strftime('%d/%m/%Y %H:%M')}"):
                    st.write(f"**Đường dẫn:** {backup['path']}")
                    st.write(f"**Kích thước:** {os.path.getsize(backup['path'])} bytes")
                    
                    if st.button("Xóa bản sao lưu", key=f"delete_{backup['name']}"):
                        try:
                            os.remove(backup['path'])
                            st.success("✅ Đã xóa bản sao lưu!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Lỗi khi xóa bản sao lưu: {str(e)}")
        else:
            st.info("Chưa có bản sao lưu nào!")
    
    with tab2:
        st.subheader("Khôi phục dữ liệu")
        st.write("Khôi phục dữ liệu từ bản sao lưu trước đó.")
        
        backup_files = get_backup_files()
        if backup_files:
            # Tạo danh sách lựa chọn
            backup_options = [f"{backup['name']} - {backup['created_at'].strftime('%d/%m/%Y %H:%M')}" 
                            for backup in backup_files]
            
            selected_backup = st.selectbox(
                "Chọn bản sao lưu để khôi phục",
                backup_options
            )
            
            if st.button("Khôi phục dữ liệu", use_container_width=True):
                # Lấy file backup được chọn
                selected_index = backup_options.index(selected_backup)
                backup_file = backup_files[selected_index]['path']
                
                # Khôi phục dữ liệu
                restored_data = restore_data(backup_file)
                if restored_data:
                    # Cập nhật dữ liệu người dùng
                    st.session_state.current_user.username = restored_data['username']
                    st.session_state.current_user.notes = restored_data['notes']
                    st.session_state.current_user.tasks = restored_data['tasks']
                    st.session_state.current_user.events = restored_data['events']
                    st.session_state.current_user.finance = restored_data['finance']
                    
                    st.success("✅ Đã khôi phục dữ liệu thành công!")
                    st.rerun()
                else:
                    st.error("❌ Không thể khôi phục dữ liệu!")
        else:
            st.info("Chưa có bản sao lưu nào để khôi phục!") 