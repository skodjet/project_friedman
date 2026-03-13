"""
User authentication and signup/login data storage
"""
import bcrypt
from typing import Tuple
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
        self.login_attempts = {} # username : [num of attempts, last attempt (timestamp)]
        self.max_attempts = 5
        self.lockout_minutes = 15

    # Returns True if user is added, False if the user already exists
    def add_user(self, username:str, password:str) -> bool:
        if username in self.users:
            return False
        
        self.users[username] = {
            'pwd_hash': hash_pwd(password),
            'created_at': datetime.now(),
            'pwd_rounds': 12
        }
        return True
    
    # Returns True if user was able to login, and login message (success or error msg)
    def login(self, username:str, password:str) -> Tuple[bool, str]:
        if self._is_locked(username):
            return False, "Too many attempts, account locked!"
        
        if username not in self.users:
            return False, "Invalid username"
        
        if not check_pwd(password, self.users[username]):
            self._increment_attempts(username)
            return False, "Invalid password"
        
        # Login successful. Clear login attempts 
        if username in self.login_attempts.keys:
            del self.login_attempts[username]
        
        return True, "Success"

    # Returns True if user account is locked (max attempts reached)
    def _is_locked(self, username:str) -> bool:
        # User has not tried to log in
        if username not in self.login_attempts:
            return False
        
        # User has tried to login. Get their # of attempts and last attempt. 
        # If their attempts exceed max attempts and timeout hasn't passed, return True
        # else return False
        attempts, last_attempt = self.login_attempts[username]
        if attempts >= self.max_attempts and ((datetime.now() - last_attempt) / 60) < self.lockout_minutes:
            return True
        
        # Lockout period expired. Reset the user's lockout data
        else:
            del self.lockout_attempts[username]
            return False
    
    # Keeps self.login_attempts dictionary updated
    def _increment_attempts(self, username:str):
        now = datetime.now()
        if username in self.login_attempts:
            attempts, _ = self.login_attempts[username]
            self.login_attempts[username] = (attempts + 1, now)

        else:
            self.login_attempts[username] = (1, now)
        
    # Updates hash. Called when num of users increases past a threshhold
    def _upgrade_hash(self, username:str, password:str):
        user = self.users[username]
        min_rounds = 14
        if user['pwd_rounds'] <= 14:
            user['pwd_hash'] = hash_pwd(user['pwd_hash'], min_rounds)
            user['pwd_rounds'] = min_rounds
