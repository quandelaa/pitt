from pitt.utils import get_vault_property
from pitt.db_handler import DB_PATH, store_password, init_db, configure_vault, get_by_properties, delete_by_password
from pitt.security import master_encrypt, derive_key, encrypt, decrypt
from os import urandom
import pytest

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    temp_db = tmp_path / 'passwords.db'

    monkeypatch.setattr("pitt.db_handler.DB_PATH", temp_db)

    init_db()

    yield temp_db

def test_add_get_del(test_db) -> None:
    m_password = "test"
    new_m_hash = master_encrypt(m_password)
    
    new_salt = urandom(16)

    configure_vault(new_salt, new_m_hash)

    _, salt = get_vault_property()
    key = derive_key(m_password, salt)

    new_password = "secretverysecretpassword"
    encrypted = encrypt(key, new_password)

    store_password("test_service", "test_username", "test_note", encrypted)

    # get
    results = get_by_properties("test_service", "test_username")

    encrypted_password = results[0][4]
    password = decrypt(key, encrypted_password).decode()

    assert password == new_password

    # del
    
    delete_by_password(encrypted_password)
    results = get_by_properties("test_service", "test_username")

    assert len(results) == 0
