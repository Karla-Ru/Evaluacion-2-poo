from proyecto.model.empleado import obtener_empleado_por_id

print("========== PRUEBA DE DESCIFRADO ==========")

try:
    id_empleado = int(input("Ingrese el ID del empleado registrado: "))

    empleado = obtener_empleado_por_id(id_empleado)

    if empleado:
        print("\n[INFO] Empleado recuperado desde Oracle:\n")
        print(empleado.mostrar_datos())

        print("\n[OK] Descifrado realizado correctamente.")

except ValueError:
    print("[WARNING] Ingrese un ID numérico válido.")

#FUNCIONA CORRECTAMENTE :D