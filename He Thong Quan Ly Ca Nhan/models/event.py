from datetime import datetime, timedelta

class Event:
    def __init__(self, title, description, start_time, end_time, event_type="Sự kiện", time_spent=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.event_type = event_type
        self.time_spent = time_spent

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "event_type": self.event_type,
            "time_spent": self.time_spent
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            event_type=data["event_type"],
            time_spent=data.get("time_spent")
        )

    def is_today(self):
        return self.start_time.date() == datetime.now().date()

    def get_duration(self):
        duration = self.end_time - self.start_time
        return int(duration.total_seconds() / 60)  # Trả về số phút

    def is_upcoming(self):
        """Kiểm tra xem sự kiện có sắp diễn ra không (trong vòng 24h)"""
        now = datetime.now()
        return self.start_time > now and (self.start_time - now) < timedelta(days=1) 