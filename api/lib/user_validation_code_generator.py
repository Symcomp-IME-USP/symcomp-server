import random

class UserValidationCodeGenerator:
    def __init__(self):
        self.code = f"{random.randint(100000, 999999)}"
        
    def generate(self):
        return self.code