from proyecto.config.app_config import conectar_db

def inicializar_roles_permisos():

    conn = conectar_db()

    if conn is None:
        print("[ERROR] No se pudo conectar a Oracle.")
        return

    cursor = None

    try:
        cursor = conn.cursor()

        # 1. CREAR ROLES SI NO EXISTEN

        roles = [
            ("ADMINISTRADOR", "Acceso a las funciones administrativas."),
            ("EMPLEADO", "Acceso a las funciones correspondientes al empleado.")
        ]

        for nombre, descripcion in roles:

            cursor.execute("""
                MERGE INTO roles destino
                USING (
                    SELECT :1 nombre, :2 descripcion
                    FROM dual
                ) origen
                ON (destino.nombre = origen.nombre)
                WHEN NOT MATCHED THEN
                    INSERT (nombre, descripcion)
                    VALUES (origen.nombre, origen.descripcion)
            """, (nombre, descripcion))

        # 2. CREAR PERMISOS SI NO EXISTEN

        permisos = [
            ("GESTIONAR_EMPLEADOS", "Administrar empleados."),
            ("GESTIONAR_DEPARTAMENTOS", "Administrar departamentos."),
            ("GESTIONAR_PROYECTOS", "Administrar proyectos."),
            ("GESTIONAR_REGISTROS_TIEMPO", "Administrar registros de tiempo."),
            ("GESTIONAR_USUARIOS", "Administrar usuarios."),
            ("CONSULTAR_INFORMES", "Consultar informes.")
        ]

        permisos_empleado = [
            ("CONSULTAR_DATOS_PROPIOS", "Permite consultar los propios datos personales y laborales."),
            ("REGISTRAR_HORAS", "Permite registrar las propias horas de trabajo."),
            ("CONSULTAR_PROYECTOS_ASIGNADOS", "Permite consultar los proyectos asignados al empleado.")
             ]

        for nombre, descripcion in permisos + permisos_empleado:

            cursor.execute("""
                MERGE INTO permisos destino
                USING (
                    SELECT :1 nombre, :2 descripcion
                    FROM dual
                ) origen
                ON (destino.nombre = origen.nombre)
                WHEN NOT MATCHED THEN
                    INSERT (nombre, descripcion)
                    VALUES (origen.nombre, origen.descripcion)
            """, (nombre, descripcion))

        # 3. OBTENER ID DEL ROL ADMINISTRADOR

        cursor.execute("""
            SELECT id_rol
            FROM roles
            WHERE nombre = 'ADMINISTRADOR'
        """)

        id_admin = cursor.fetchone()[0]

        # 4. ASIGNAR LOS SEIS PERMISOS AL ADMINISTRADOR

        for nombre, descripcion in permisos:

            cursor.execute("""
                SELECT id_permiso
                FROM permisos
                WHERE nombre = :1
            """, (nombre,))

            id_permiso = cursor.fetchone()[0]

            cursor.execute("""
                MERGE INTO rol_permiso destino
                USING (
                    SELECT :1 id_rol, :2 id_permiso
                    FROM dual
                ) origen
                ON (
                    destino.id_rol = origen.id_rol
                    AND destino.id_permiso = origen.id_permiso
                )
                WHEN NOT MATCHED THEN
                    INSERT (id_rol, id_permiso)
                    VALUES (origen.id_rol, origen.id_permiso)
            """, (id_admin, id_permiso))

        #OBTENER ID DEL ROL EMPLEADO

        cursor.execute("""
            SELECT id_rol
            FROM roles
            WHERE nombre = 'EMPLEADO'
        """)

        id_rol_empleado = cursor.fetchone()[0]

        #ASIGNAR PERMISOS AL EMPLEADO

        for nombre, descripcion in permisos_empleado:

            cursor.execute("""
                SELECT id_permiso
                FROM permisos
                WHERE nombre = :1
            """, (nombre,))

            id_permiso = cursor.fetchone()[0]

            cursor.execute("""
                MERGE INTO rol_permiso destino
                USING (
                    SELECT :1 id_rol, :2 id_permiso
                    FROM dual
                ) origen
                ON (
                    destino.id_rol = origen.id_rol
                    AND destino.id_permiso = origen.id_permiso
                )
                WHEN NOT MATCHED THEN
                    INSERT (id_rol, id_permiso)
                    VALUES (origen.id_rol, origen.id_permiso)
            """, (id_rol_empleado, id_permiso))

        # CONFIRMAR CAMBIOS

        conn.commit()

        print("[INFO] Roles registrados correctamente.")
        print("[INFO] Permisos registrados correctamente.")
        print("[INFO] Permisos asignados al administrador.")
        print("[INFO] Permisos asignados al empleado.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] No se pudieron inicializar los datos: {e}")

    finally:
        if cursor is not None:
            cursor.close()

        conn.close()

if __name__ == "__main__":
    inicializar_roles_permisos()