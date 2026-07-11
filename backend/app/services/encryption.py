from cryptography.fernet import Fernet

from app.core.config import settings

fernet = Fernet(settings.FERNET_KEY.encode())


def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode()).decode()