from datetime import datetime

class Note:
    def __init__(self, title, content, category=None, tags=None, created_at=None, updated_at=None):
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            content=data["content"],
            category=data.get("category"),
            tags=data.get("tags", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def update(self, title=None, content=None, category=None, tags=None):
        if title:
            self.title = title
        if content:
            self.content = content
        if category:
            self.category = category
        if tags:
            self.tags = tags
        self.updated_at = datetime.now() 