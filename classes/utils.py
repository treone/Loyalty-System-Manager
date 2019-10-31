import base64
import random
import zlib


def encrypt(password):
    """Зашифровать пароль для хранения в настройках"""
    used_chars = list(set([c for c in password if not c.isspace()]))
    if used_chars:
        random.shuffle(used_chars)
        salt = used_chars[:2]
    else:
        salt = []
    while len(salt) < 3:
        c = chr(random.randint(0, 127))
        if not c.isspace():
            salt.insert(0, c)
    salt = ''.join(salt)
    string_to_encrypt = salt + '\n' + password
    compressed = zlib.compress(bytes(string_to_encrypt, "utf-8"), 9)
    while len(compressed) % 3:
        compressed += bytes(chr(random.randint(0, 127)), "utf-8")
    return '#1##' + base64.b64encode(compressed).decode("utf-8")


def decrypt(password):
    """Расшифровать сохраненный в настройках пароль"""
    if not password.startswith('#1##'):
        raise ValueError('Ошибка при расшифровке сохраненного пароля.')
    return zlib.decompress(base64.b64decode(password[4:].encode("utf-8"))).decode("utf-8").split('\n', 1)[-1]
