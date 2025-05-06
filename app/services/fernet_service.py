from cryptography.fernet import Fernet
from settings import get_settings


class FernetService:
    def __init__(self, fernet_key: str):
        self.key = fernet_key
        self.worker = Fernet(self.key)

    def encode_str(self, value: str) -> str:
        message_bytes = value.encode()
        encrypted_message = self.worker.encrypt(message_bytes)
        return encrypted_message.decode()

    def decode_str(self, value: str) -> str:
        encrypted_message_bytes = value.encode()
        decrypted_message = self.worker.decrypt(encrypted_message_bytes)
        return decrypted_message.decode()


def get_fernet() -> FernetService:
    return FernetService(get_settings().FERNET_CRYPT_KEY)
