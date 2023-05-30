class Task:
    task : str = None
    answear : str = None
    timestamp = None
    points : int = None
    id : int = None
    classroom : str = None
    def __init__(self,task : str, answear : str,id_ : int,classroom_ : str):
        self.task = task
        self.answear = answear
        points = 2
        self.id = id_
        self.classroom = classroom_



