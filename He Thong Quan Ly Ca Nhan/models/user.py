class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
        self.notes = []
        self.personal_info = {
            'name': '',
            'phone': '',
            'address': ''
        } 