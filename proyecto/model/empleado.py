from proyecto.config.app_config import conectar_db, oracledb

def validar_tabla_empleado():

    consulta_sql = """
        CREATE TABLE empleados (
            id_empleado NUMBER GENERATED ALWAYS AS IDENTITY
                (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(100) NOT NULL,
            direccion VARCHAR2(200),
            telefono VARCHAR2(30),
            correo_electronico VARCHAR2(100) NOT NULL,
            fecha_contratacion DATE NOT NULL,
            salario NUMBER(12,2) NOT NULL,
            activo NUMBER(1) DEFAULT 1 NOT NULL,
            CONSTRAINT uq_empleado_correo
                UNIQUE (correo_electronico),
            CONSTRAINT ck_empleado_salario
                CHECK (salario > 0),
            CONSTRAINT ck_empleado_activo
                CHECK (activo IN (0,1))
        )
    """

    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            # Oracle (bd): ejecutar solo si la tabla no existe
            cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE :sql;
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE != -955 THEN
                            RAISE;
                        END IF;
                END;
            """, {"sql": consulta_sql})

            print("[INFO] Tabla empleados validada correctamente")

    except Exception as e:
        print(f"[ERROR] Creación de tabla empleados | {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insertar_datos_empleado(empleado: Empleado):

    consulta_insert = """
        INSERT INTO empleados
        (nombre, direccion, telefono, correo_electronico,
         fecha_contratacion, salario, activo)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
    """

    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            cursor.execute(
                consulta_insert,
                (
                    empleado.nombre,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.correo_electronico,
                    empleado.fecha_contratacion,
                    empleado.salario,
                    int(empleado.activo)
                )
            )

            conn.commit()
            print("[INFO] Empleado registrado correctamente")

    except oracledb.IntegrityError as e:

        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] Ya existe un empleado con ese correo")
        else:
            print(f"[ERROR] Error de integridad | {e}")

    except Exception as e:

        if conn:
            conn.rollback()

        print(f"[ERROR] Empleado no registrado | {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

class EmpleadoRepositorio():

    def __init__(self):
        pass

    def actualizar_salario(self, nuevo_salario: float):

        if isinstance(nuevo_salario, (int, float)) and nuevo_salario > 0:

            consulta_update = """
                UPDATE empleados
                SET salario = :1
                WHERE id_empleado = :2
            """

            conn = None
            cursor = None

            try:
                conn = conectar_db()

                if conn:
                    cursor = conn.cursor()

                    cursor.execute(
                        consulta_update,
                        (nuevo_salario, self.id_empleado)
                    )

                    conn.commit()

                    if cursor.rowcount > 0:
                        self.salario = nuevo_salario
                        print("[INFO] Salario actualizado correctamente")
                    else:
                        print("[WARNING] Empleado no encontrado")

            except Exception as e:

                if conn:
                    conn.rollback()

                print(f"[ERROR] No se pudo actualizar el salario | {e}")

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        else:
            print("[WARNING] Salario no válido")

    def cambiar_estado(self, estado: bool):

        consulta_update = """
            UPDATE empleados
            SET activo = :1
            WHERE id_empleado = :2
        """

        conn = None
        cursor = None

        try:
            conn = conectar_db()

            if conn:
                cursor = conn.cursor()

                cursor.execute(
                    consulta_update,
                    (int(estado), self.id_empleado)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    self.activo = estado
                    print("[INFO] Estado actualizado correctamente")
                else:
                    print("[WARNING] Empleado no encontrado")

        except Exception as e:

            if conn:
                conn.rollback()

            print(f"[ERROR] No se pudo cambiar el estado | {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

class Empleado(EmpleadoRepositorio):

    def __init__(
        self,
        nombre: str,
        direccion: str,
        telefono: str,
        correo_electronico: str,
        fecha_contratacion,
        salario: float
    ):

        self.id_empleado = None
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.fecha_contratacion = fecha_contratacion
        self.salario = salario
        self.activo = True

    def mostrar_datos(self):

        return (
            f"Empleado\n"
            f"ID: {self.id_empleado}\n"
            f"Nombre: {self.nombre}\n"
            f"Dirección: {self.direccion}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo_electronico}\n"
            f"Fecha contratación: {self.fecha_contratacion}\n"
            f"Salario: {self.salario}\n"
            f"Activo: {self.activo}"
        )