import json
from pathlib import Path
from .user import User

class AuthManager:
    def __init__(self):
        self.users_file = Path("data/users.json")
        self.users_file.parent.mkdir(exist_ok=True)
        self.users = self._load_users()

    def _load_users(self):
        """Tải danh sách người dùng từ file"""
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        """Lưu danh sách người dùng vào file"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def register(self, username, password):
        """Đăng ký người dùng mới"""
        if username in self.users:
            return False, "Tên đăng nhập đã tồn tại"
        
        self.users[username] = {
            'password': password,
            'tasks': [],
            'notes': [],
            'personal_info': {
                'name': '',
                'phone': '',
                'address': ''
            }
        }
        self._save_users()
        return True, "Đăng ký thành công"

    def login(self, username, password):
        """Đăng nhập"""
        if username not in self.users:
            return False, "Tên đăng nhập không tồn tại"
        
        if self.users[username]['password'] != password:
            return False, "Mật khẩu không đúng"
        
        return True, "Đăng nhập thành công"

    def get_user(self, username):
        """Lấy thông tin người dùng"""
        if username in self.users:
            user_data = self.users[username]
            user = User(username, user_data['password'])
            user.tasks = user_data['tasks']
            user.notes = user_data['notes']
            user.personal_info = user_data['personal_info']
            return user
        return None 