from proyecto.model.rol import (
    validar_tabla_rol,
    validar_tabla_rol_permiso
)

from proyecto.model.permiso import (
    validar_tabla_permiso
)

def main():

    print("\n========== CREACIÓN DE TABLAS ==========\n")

    # 1. CREAR RABLA ROLES
    validar_tabla_rol()

    # 2. CREAR T PERMISOS
    validar_tabla_permiso()

    # 3. CREAR T INTERMEDIA
    validar_tabla_rol_permiso()

    print("\n========== PROCESO FINALIZADO ==========")

if __name__ == "__main__":
    main()