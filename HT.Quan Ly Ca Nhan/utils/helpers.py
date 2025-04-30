import json
from datetime import datetime

def save_data(data, filename):
    """Lưu dữ liệu vào file JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(filename):
    """Đọc dữ liệu từ file JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def format_date(date):
    """Định dạng ngày tháng"""
    return date.strftime('%d/%m/%Y %H:%M:%S') 