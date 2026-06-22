from pwdlib import PasswordHash

class PasswordManager:
    _password_hash = PasswordHash.recommended()

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._password_hash.hash(password)
    
    @classmethod
    def verify(cls, password: str, password_hashed: str) -> bool:
        return cls._password_hash.verify(password, password_hashed)