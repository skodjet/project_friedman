"""
User authentication and signup/login data storage
"""

import bcrypt
from datetime import datetime

# Handler functions
def hash_pwd(password:str, rounds=12) -> bytes:
    pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    print(pwd)
    return pwd


def check_pwd(password:str, hash:bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash)


class UserAuth:
    def __init__(self):
        self.users = {} # TODO: replace with SQLAlchemy DB
        self.login_attempts = {} # {num of attempts : last attempt}
        self.max_attempts = 5
        self.lockout_minutes = 15

    def add_user(self, username:str, password:str) -> bool:
        if username in self.users:
            return False
        
        self.users[usernmae] = {
            'pwd_hash': hash_pwd(password),
            'created_at': datetime.now(),
            'pwd_rounds': 12
        }
        return True
    
    def login(self):
        pass

    def _is_locked(self, username:str) -> bool:
        if username not in self.login_attempts:
            return False
        
        attempts, last_attempt = self.login_attempts[username]
        
