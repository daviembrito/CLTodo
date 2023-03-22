from datetime import datetime

class Task():
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.created_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.done = False
        self.done_date = None
        self.id = None