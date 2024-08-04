import keyring
from keyring.errors import PasswordDeleteError, PasswordSetError
import tempfile
from pathlib import Path
from dataclasses import dataclass
from cryptography.fernet import Fernet

@dataclass
class FernetKeyringTempfile:
    application_name: str

    def get_temp_file_path(self) -> Path:
        return Path(tempfile.gettempdir()) / f"fkt_{self.application_name}"

    def get_keyring_service_name(self) -> str:
        return f"fernet_keyring_tempfile.py_{self.application_name}"
    
    def get_keyring_username(self) -> str:
        return "key"

    def get_or_create_key(self) -> bytes:
        try:
            key_existing = keyring.get_password(
                service_name = self.get_keyring_service_name(),
                username     = self.get_keyring_username(),
            )
            if key_existing is not None:
                return key_existing.encode("utf-8")
            else:
                key_fresh = Fernet.generate_key()
                keyring.set_password(
                    service_name = self.get_keyring_service_name(),
                    username     = self.get_keyring_username(),
                    password     = key_fresh.decode("utf-8"),
                )
                return key_fresh
        except PasswordSetError as e:
            raise ValueError(
                "Unable to set password using keyring for some reason"
            ) from e

    def store(self, data_plaintext: bytes) -> None:
        with self.get_temp_file_path().open("wb") as temp_file:
            key = self.get_or_create_key()
            data_encrypted = Fernet(key).encrypt(data_plaintext)
            temp_file.write(data_encrypted)

    def load(self) -> bytes:
        with self.get_temp_file_path().open("rb") as temp_file:
            key_existing = keyring.get_password(
                service_name = self.get_keyring_service_name(),
                username     = self.get_keyring_username()
            )
            if key_existing is None:
                raise ValueError("No key found in keyring")
            data_encrypted = temp_file.read()
            data_plaintext = Fernet(key_existing.encode("utf-8")).decrypt(
                data_encrypted
            )
            return data_plaintext

    def remove(self, missing_ok=True) -> None:
        self.get_temp_file_path().unlink(missing_ok=missing_ok)
        try:
            keyring.delete_password(
                service_name = self.get_keyring_service_name(),
                username     = self.get_keyring_username()
            )
        except PasswordDeleteError as e:
            if not missing_ok:
                raise ValueError(
                    "Unable to delete password using keyring for some reason"
                ) from e
