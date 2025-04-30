import json
import os
from datetime import datetime
import streamlit as st

def backup_data(user_data):
    """
    Tạo bản sao lưu dữ liệu người dùng
    """
    try:
        # Tạo thư mục backup nếu chưa tồn tại
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Tạo tên file backup với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/backup_{timestamp}.json"
        
        # Lưu dữ liệu vào file
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)
        
        return backup_file
    except Exception as e:
        st.error(f"Lỗi khi sao lưu dữ liệu: {str(e)}")
        return None

def restore_data(backup_file):
    """
    Khôi phục dữ liệu từ file backup
    """
    try:
        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Lỗi khi khôi phục dữ liệu: {str(e)}")
        return None

def get_backup_files():
    """
    Lấy danh sách các file backup
    """
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        return []
    
    backup_files = []
    for file in os.listdir(backup_dir):
        if file.endswith(".json"):
            file_path = os.path.join(backup_dir, file)
            backup_files.append({
                "name": file,
                "path": file_path,
                "created_at": datetime.fromtimestamp(os.path.getctime(file_path))
            })
    
    # Sắp xếp theo thời gian tạo mới nhất
    return sorted(backup_files, key=lambda x: x["created_at"], reverse=True) 