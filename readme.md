# Fernet Keyring Tempfile

> WARNING: you should read the source code and understand this package, or do
> not use it. If you do choose to use it, then that is at your own risk. It is a
> naive and simple secret storage system. The main purpose is to avoid storing
> plaintext tokens on disk between python notebook sessions.
>
> A better solution would be to use the `keyring` package directly, but on
> windows there is some
> [silly limit on the size of a password (1280 characters?)](https://github.com/jaraco/keyring/issues/355)
> that means I need to save my secret to disk instead.
>
> When used as demonstrated below it does not guard against any serious attack,
> rather, it might stop a hypothetical file system scan from detecting an
> unencrypted token stored on disk. If an attacker has remote code execution,
> and can run a python script under your Username, then they can retrieve the
> secret as easily as you can by running the code similar to the example below.
> However if their process is running under another username, or they just got
> access to your storage device without remote code execution, then perhaps this
> method offers some level of protection.

This package uses `cryptography.Fernet().encrypt()` to encrypt and store a file
in your machines temporary folder (determined using `tempfile.gettempdir()`).
The key is generated using `cryptography.Fernet.generate_key()` and is
automatically stored in your system's secret storage using
`keyring.set_password()`.

```python
from fernet_keyring_tempfile import FernetKeyringTempfile

(
    FernetKeyringTempfile(
        application_name="TEST_APPLICATION_NAME"
    )
    .store("SECRET MESSAGE!".encode("utf-8"))
)
```

Later:
```python
from fernet_keyring_tempfile import FernetKeyringTempfile

print(
    FernetKeyringTempfile(
        application_name"TEST_APPLICATION_NAME"
    )
    .load()
    .decode("utf-8")
)
# >> "SECRET MESSAGE!"
```

Note that if the passphrase (e.g. `"TEST_APPLICATION_NAME"`) appears in
plaintext in the example above then there is a hole in security since the
attacker can presumably also see your source code.
