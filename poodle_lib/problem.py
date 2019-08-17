from poodle import schedule, SchedulingError

class Problem:
    def __init__(self):
        self.plan = None
    def run(self):
        try:
            self.plan = schedule(
                methods=[getattr(self,m) for m in dir(self) if callable(getattr(self,m))], 
                space=self.__dict__.values(),
                exit=self.exit
            )
        except SchedulingError:
            pass