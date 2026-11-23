import bcrypt

from proyecto.security.seguridad_contraseñas import (
    generar_hash,
    verificar_hash,
    necesita_actualizacion
)

print("\n========== PRUEBAS DE SEGURIDAD ==========")

# PRUEBA 1: GENERAR HASH ARGON2ID

clave = "ClavePrueba123!"

hash_argon = generar_hash(clave)

if hash_argon.startswith("$argon2id$"):
    print("[OK] Generación de hash Argon2id.")
else:
    print("[ERROR] El hash generado no es Argon2id.")

#PRUEBA 2: VERIFICAR CONTRASEÑA CORRECTA

if verificar_hash(clave, hash_argon):
    print("[OK] Verificación de contraseña correcta.")
else:
    print("[ERROR] No se pudo verificar la contraseña.")

#PRUEBA 3: VERIFICAR CONTRASEÑA INCORRECTA

if not verificar_hash("ClaveIncorrecta", hash_argon):
    print("[OK] Rechazo de contraseña incorrecta.")
else:
    print("[ERROR] Se aceptó una contraseña incorrecta.")

#PRUEBA 4: COMPATIBILIDAD CON BCRYPT

hash_bcrypt = bcrypt.hashpw(
    clave.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

if verificar_hash(clave, hash_bcrypt):
    print("[OK] Verificación de hash bcrypt antiguo.")
else:
    print("[ERROR] Falló la verificación bcrypt.")

#PRUEBA 5: DETECTAR HASHES QUE NECESITAN MIGRACIÓN

if necesita_actualizacion(hash_bcrypt):
    print("[OK] Detección de hash bcrypt para migración.")
else:
    print("[ERROR] No se detectó el hash bcrypt.")

if not necesita_actualizacion(hash_argon):
    print("[OK] Hash Argon2id no necesita migración.")
else:
    print("[ERROR] Se indicó una migración innecesaria.")

print("\n========== PRUEBAS FINALIZADAS ==========")