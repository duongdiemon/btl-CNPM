from datetime import datetime

class Task:
    def __init__(self, title, description, due_date=None, priority="Trung bình", status="Chưa hoàn thành"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = datetime.now()
        self.completed_at = None

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            status=data['status']
        )
        if data['due_date']:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        task.created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
        if data['completed_at']:
            task.completed_at = datetime.strptime(data['completed_at'], '%Y-%m-%d %H:%M:%S')
        return task 