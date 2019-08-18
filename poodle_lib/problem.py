from poodle import schedule, goal
from poodle.schedule import SchedulingError

class Problem:
    def __init__(self):
        self.plan = None
        self.objectList = []
    def addObject(self, obj):
        self.objectList.append(obj)
        return obj
    def run(self):
        self.problem()
        try:
            self.plan = schedule(
                methods=[getattr(self,m) for m in dir(self) if callable(getattr(self,m))], 
                space=list(self.__dict__.values())+self.objectList,
                goal=goal(self.goal())
                #exit=self.exit
            )
        except SchedulingError:
            pass