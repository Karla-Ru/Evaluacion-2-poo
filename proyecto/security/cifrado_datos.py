import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken

#CARGAR LAS VARIABLES DEL .env 
load_dotenv()

#OBTENER LA CLAVE SECRETA
CLAVE_FERNET = os.getenv("FERNET_KEY")

def obtener_cifrador():
    """
    Crea el objeto Fernet utilizando la clave
    almacenada en las variables de entorno.
    """
    if not CLAVE_FERNET:
        raise RuntimeError(
            "No se encontró FERNET_KEY en el archivo .env."
        )

    try:
        return Fernet(CLAVE_FERNET.encode("utf-8"))
    except (ValueError, TypeError):
        raise RuntimeError(
            "La clave FERNET_KEY no tiene un formato válido."
        )

def cifrar_dato(dato):
    """
    Cifra un dato de texto y devuelve el resultado
    como una cadena de caracteres.
    """
    if dato is None:
        return None

    if not isinstance(dato, str):
        raise TypeError("El dato que se desea cifrar debe ser texto.")

    if dato == "":
        return ""

    cifrador = obtener_cifrador()

    dato_bytes = dato.encode("utf-8")
    dato_cifrado = cifrador.encrypt(dato_bytes)

    return dato_cifrado.decode("utf-8")

def descifrar_dato(dato_cifrado):
    """
    Descifra un dato previamente cifrado con Fernet.
    """
    if dato_cifrado is None:
        return None

    if dato_cifrado == "":
        return ""

    cifrador = obtener_cifrador()

    try:
        dato_bytes = dato_cifrado.encode("utf-8")
        dato_descifrado = cifrador.decrypt(dato_bytes)

        return dato_descifrado.decode("utf-8")

    except InvalidToken:
        raise ValueError(
            "No fue posible descifrar el dato. "
            "La clave puede ser incorrecta o el contenido estar alterado."
        )