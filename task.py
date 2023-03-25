from datetime import datetime

class Task():
    def __init__(self, position, name, category, created_date, done_date, done):
        self.position = position
        self.name = name
        self.category = category
        self.created_date = created_date
        self.done = False
        self.done_date = None

    @classmethod
    def create(cls, name, category):
        position = -1
        created_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S.%f")
        done = False
        done_date = None
        return cls(position, name, category, created_date, done_date, done)