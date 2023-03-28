from datetime import datetime

class Todo():
    def __init__(self, position:int, name:str, category:str, created_date:str, done_date:str, done:bool):
        self.position = position
        self.name = name
        self.category = category
        self.created_date = created_date
        self.done = done
        self.done_date = done_date

    @classmethod
    def create(cls, name:str, category:str):
        position = -1
        created_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S.%f")
        done = False
        done_date = None
        return cls(position, name, category, created_date, done_date, done)