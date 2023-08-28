import pytest
from toolbox.core.rsakey import RSAKey, encrypt


def test_rsa_public_key():
    """Test the rsa public key."""
    rsa_key = RSAKey()
    assert isinstance(rsa_key.get_public_key(), str)
    assert "-----BEGIN PUBLIC KEY-----" in rsa_key.get_public_key()
    assert "-----END PUBLIC KEY-----" in rsa_key.get_public_key()


def test_rsa_encrypt_decrypt():
    """Test the rsa decrypt."""
    rsa_key = RSAKey()
    message = "test message"
    encrypted_message = encrypt(message, rsa_key.get_public_key().encode("utf-8"))
    assert isinstance(encrypted_message, str)
    assert rsa_key.decrypt(encrypted_message) == message


def test_rsa_encrypt_decrypt_wrong_key():
    """Test the rsa decrypt."""
    rsa_key = RSAKey()
    message = "test message"
    fake_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtvJ04pfTQiuV2pLR2NXm
0xrgIKfE62aYwirKoCPLr63HeNW6vgj8GT+FKw+qoBVjmkGZOFHQvgeAsTlVO5gp
jXBXavW62v4pv5Q+aTUR/bJu8N8xcZ8r4165nUWPajM0MMkLkcngyFg1Z5WSntCO
sGQcf07vzuqai4o4AttAwAGKnOP3TAbdqnX1Hg53c6f8QJvHfX0FB1Z+otWm+FYw
I97fxgGYuZkRhcANhXEEHhZ0s8f06jTwX7/xhJyJ8khiMvCaNxxa8HZ2qnSiACHi
ZL5oEVHSIBlxPlkNYF3OMMTsZWEBqE0DZsugVgQLCdp4rhlfO+Jv7E6scK8m6C/m
gwIDAQAB
-----END PUBLIC KEY-----
"""
    encrypted_message = encrypt(message, fake_key.encode("utf-8"))
    assert isinstance(encrypted_message, str)
    with pytest.raises(ValueError):
        rsa_key.decrypt(encrypted_message)


def test_rsa_encrypt_decrypt_wrong_message():
    """Test the rsa decrypt."""
    rsa_key = RSAKey()
    message = "test message"
    encrypted_message = encrypt(message, rsa_key.get_public_key().encode("utf-8"))
    assert isinstance(encrypted_message, str)
    with pytest.raises(ValueError):
        rsa_key.decrypt("wrong message")
