
from fernet_keyring_tempfile import FernetKeyringTempfile
import keyring

def test_fkt():
    thing = FernetKeyringTempfile("TEST_CRYPT")
    thing.store(b"BONKERS!")
    thing.get_temp_file_path().exists()
    assert thing.get_temp_file_path().read_bytes() != b"BONKERS!"
    assert keyring.get_password(
        service_name = thing.get_keyring_service_name(),
        username     = thing.get_keyring_username(),
    ) is not None
    assert thing.load() == b"BONKERS!"

    thing.remove()

    assert not thing.get_temp_file_path().exists()
    assert keyring.get_password(
        service_name = thing.get_keyring_service_name(),
        username     = thing.get_keyring_username(),
    ) is None
