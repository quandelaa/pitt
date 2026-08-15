from pitt.security import encrypt, decrypt, derive_key, master_encrypt, verify_master_password
from os import urandom

def test_encryption_decryption() -> None:
    master_password = "master123"
    salt  = urandom(16)
    
    key = derive_key(master_password, salt)
    password = "password123"

    encrypted = encrypt(key, password)
    decrypted = decrypt(key, encrypted).decode()

    assert decrypted == password

def test_master_verify() -> None:
    master_password = "master123"

    hash = master_encrypt(master_password)
    verify = verify_master_password(master_password, hash)

    assert verify == True
