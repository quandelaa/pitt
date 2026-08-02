from argon2 import PasswordHasher, exceptions, low_level, Type
from cryptography.fernet import Fernet
import base64
import os

def master_encrypt(password: str) -> str:
    """
    Returns the encrypted hash of a given master password
    """

    kdf = PasswordHasher()
    hash = kdf.hash(password)

    return hash

def verify_master_password(password: str, hash: str) -> bool:
    """
    Verifies whether the inputted master password matches with the stored master password
    """
    
    kdf = PasswordHasher()

    try:
        kdf.verify(hash, password)
    except exceptions.VerifyMismatchError:
        return False

    return True

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives the 64-byte Argon2id key from the password
    """

    key = low_level.hash_secret_raw(password.encode("utf-8"), salt, 3, 65536, 1, 32, Type.ID)

    b64_key = base64.urlsafe_b64encode(key)

    return b64_key

def encrypt(key: bytes, password: str) -> bytes:
    """
    Encrypts the given password using Fernet
    """

    f = Fernet(key)
    token = f.encrypt(password.encode("utf-8"))

    return token

def decrypt(key: bytes, encrypted: bytes) -> bytes:
    """
    Decrypts the given encrypted password using Fernet
    """

    f = Fernet(key)
    password = f.decrypt(encrypted)

    return password
