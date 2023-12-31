"""RSA key class for secure communication with frontend."""

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import cryptography.hazmat.primitives.asymmetric.rsa as rsa
from pydantic import BaseModel


class RSAKey(BaseModel):
    """
    Base class for handling the rsa keys secure communication with frontend.

    Attributes:
        __private_key (rsa.RSAPrivateKey): The private key.
        __public_key (rsa.RSAPublicKey): The public key.
    """

    def __new__(cls) -> "RSAKey":
        """Return the singleton instance."""
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Initialize the rsa keys."""
        super().__init__()

    __private_key: rsa.RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )

    __public_key: rsa.RSAPublicKey = __private_key.public_key()

    def get_public_key(self) -> str:
        """Return the public key."""
        return self.__public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def decrypt(self, package: str) -> str:
        """
        Decrypt the package.

        Args:
            package (str): The package to decrypt.
        Returns:
            str: The decrypted package.
        """
        package_decoded = base64.b64decode(package)
        decrypted_message = self.__private_key.decrypt(
            package_decoded,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return decrypted_message.decode("utf-8")


def encrypt(message: str, encryption_key: bytes) -> str:
    """
    Encrypt the message.

    Args:
        message (str): The message to encrypt.
        encryption_key (bytes): The encryption key.
    Returns:
        str: The encrypted message.
    """
    key = serialization.load_pem_public_key(encryption_key)
    encrypted_message = key.encrypt(
        message.encode("utf-8"),
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(encrypted_message).decode("utf-8")
