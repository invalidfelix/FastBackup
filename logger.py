from dateime import datetime

class Logger:
    def __init__(self, file_name):
        self.file = open(file_name, "a")
    
    def log(self, log_level, message):
        log_msh = f"[{datetime.now()}] {log_level}: {message}"
        self.file.write(f"{log_msg}\n")
        print(f"\n{log_msg}\n")
    
    def close(self):
        self.file.close()