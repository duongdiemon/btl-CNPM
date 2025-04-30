from datetime import datetime
from typing import Optional, Dict, Any

class UserProfile:
    def __init__(
        self,
        username: str,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        gender: Optional[str] = None,
        avatar: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.birth_date = birth_date
        self.gender = gender
        self.avatar = avatar
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi object thành dictionary"""
        return {
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "birth_date": self.birth_date.strftime("%Y-%m-%d") if self.birth_date else None,
            "gender": self.gender,
            "avatar": self.avatar,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Tạo object từ dictionary"""
        try:
            birth_date = datetime.strptime(data.get("birth_date", ""), "%Y-%m-%d") if data.get("birth_date") else None
            created_at = datetime.strptime(data.get("created_at", ""), "%Y-%m-%d %H:%M:%S") if data.get("created_at") else None
            updated_at = datetime.strptime(data.get("updated_at", ""), "%Y-%m-%d %H:%M:%S") if data.get("updated_at") else None
            
            return cls(
                username=data.get("username", ""),
                full_name=data.get("full_name"),
                email=data.get("email"),
                phone=data.get("phone"),
                address=data.get("address"),
                birth_date=birth_date,
                gender=data.get("gender"),
                avatar=data.get("avatar"),
                created_at=created_at,
                updated_at=updated_at
            )
        except Exception as e:
            # Nếu có lỗi khi parse datetime, tạo object mới với thời gian hiện tại
            return cls(username=data.get("username", ""))

    def update(
        self,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        gender: Optional[str] = None,
        avatar: Optional[str] = None
    ) -> None:
        """Cập nhật thông tin profile"""
        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
        if birth_date is not None:
            self.birth_date = birth_date
        if gender is not None:
            self.gender = gender
        if avatar is not None:
            self.avatar = avatar
        
        self.updated_at = datetime.now()

    def validate(self) -> bool:
        """Kiểm tra tính hợp lệ của dữ liệu"""
        if not self.username:
            return False
        
        if self.email and "@" not in self.email:
            return False
            
        if self.phone and not self.phone.isdigit():
            return False
            
        if self.gender and self.gender not in ["Nam", "Nữ", "Khác"]:
            return False
            
        return True 