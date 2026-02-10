from datetime import datetime
log_path: str = "./log.txt"

class Log:
    def __init__(self, log_path:str = log_path) -> None:
        self.log_path = log_path

    def write(self, msg:str) -> None:
        with open(self.log_path, "a") as f:
            now: datetime = datetime.now()
            f.write(str(now) + " - ")
            f.write(msg+'\n')
