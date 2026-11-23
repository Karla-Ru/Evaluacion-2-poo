from proyecto.model.rol import verificar_permiso

def main():

    print("\n========== VERIFICACIÓN DE PERMISOS ==========")

    # PRUEBAS DEL ADMINISTRADOR

    print("\n--- ADMINISTRADOR ---")

    print(
        "Gestionar empleados:",
        verificar_permiso("ADMINISTRADOR", "GESTIONAR_EMPLEADOS")
    )

    print(
        "Registrar horas:",
        verificar_permiso("ADMINISTRADOR", "REGISTRAR_HORAS")
    )

    #PRUEBAS DEL EMPLEADO

    print("\n--- EMPLEADO ---")

    print(
        "Consultar datos propios:",
        verificar_permiso("EMPLEADO", "CONSULTAR_DATOS_PROPIOS")
    )

    print(
        "Registrar horas:",
        verificar_permiso("EMPLEADO", "REGISTRAR_HORAS")
    )

    print(
        "Gestionar empleados:",
        verificar_permiso("EMPLEADO", "GESTIONAR_EMPLEADOS")
    )

if __name__ == "__main__":
    main()