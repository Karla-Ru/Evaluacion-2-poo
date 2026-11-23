import bcrypt

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)

# CONFIGURACIÓN DE AARGON2ID
_hasher = PasswordHasher()

def generar_hash(clave: str) -> str:
    """
    Genera un hash seguro utilizando Argon2id.
    """

    if not clave:
        raise ValueError("La contraseña no puede estar vacía.")

    return _hasher.hash(clave)

def verificar_hash(clave: str, clave_hash: str) -> bool:
    """
    Verifica contraseñas Argon2id o bcrypt antiguas.
    """

    if not clave or not clave_hash:
        return False

    #DETECTAR HASHES BCRYPT ANTIGUOS (CUENTAS YA CREADAS SEGUIRÁN FUNCIONANDO)
    if clave_hash.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            return bcrypt.checkpw(
                clave.encode("utf-8"),
                clave_hash.encode("utf-8")
            )
        except (ValueError, TypeError):
            return False

    #VERIFICAR HASHES ARGON2ID
    try:
        return _hasher.verify(clave_hash, clave)

    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError
    ):
        return False

def necesita_actualizacion(clave_hash: str) -> bool:
    """
    Indica si el hash debe actualizarse a Argon2id.
    """

    return clave_hash.startswith(("$2a$", "$2b$", "$2y$"))