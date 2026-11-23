from proyecto.model.rol import obtener_permisos_rol

def main():

    print("\n========== CONSULTA DE PERMISOS ==========")

    # CONSULTAR ADMINISTRADOR
    permisos_admin = obtener_permisos_rol("ADMINISTRADOR")

    print("\nPERMISOS DEL ADMINISTRADOR:")

    for permiso in permisos_admin:
        print(f"- {permiso}")

    # CONSULTAR EMPLEADO
    permisos_empleado = obtener_permisos_rol("EMPLEADO")

    print("\nPERMISOS DEL EMPLEADO:")

    if permisos_empleado:
        for permiso in permisos_empleado:
            print(f"- {permiso}")
    else:
        print("El empleado todavía no tiene permisos asignados.")

    print("\n========== FIN DE LA PRUEBA ==========")

if __name__ == "__main__":
    main()