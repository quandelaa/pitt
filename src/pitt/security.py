from argon2 import PasswordHasher, exceptions 
from cryptography.fernet import Fernet
import os

def encrypt(password: str) -> str:
    kdf = PasswordHasher()
    hash = kdf.hash(password)

    return hash

def verify_password(password: str, hash: str) -> bool:
    kdf = PasswordHasher()

    try:
        kdf.verify(hash, password)
    except exceptions.VerifyMismatchError:
        return False

    return True
