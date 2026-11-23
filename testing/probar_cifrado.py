from proyecto.security.cifrado_datos import (
    cifrar_dato,
    descifrar_dato
)

dato_original = "Puerto Montt, Chile"

print("========== PRUEBA DE CIFRADO ==========")

dato_cifrado = cifrar_dato(dato_original)

print("Dato original:", dato_original)
print("Dato cifrado:", dato_cifrado)

dato_descifrado = descifrar_dato(dato_cifrado)

print("Dato descifrado:", dato_descifrado)

if dato_original == dato_descifrado:
    print("\n[OK] El cifrado y descifrado funcionan correctamente.")
else:
    print("\n[ERROR] Los datos no coinciden.")

#FUNCIONA CORRECTAMENTE. AHORA HAY QUE PROTEGER DIRECCIÓN Y TELÉFONO

