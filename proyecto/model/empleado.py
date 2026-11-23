from __future__ import annotations #SE AGREGA PARA EVITAR REDUNDANCIA AL INSERTAR DATOS DE EMPLEADO
from proyecto.config.app_config import conectar_db, oracledb
from proyecto.security.cifrado_datos import cifrar_dato, descifrar_dato

def insertar_datos_empleado(empleado: Empleado):

    consulta_insert = """
        INSERT INTO empleados
        (nombre, direccion, telefono, correo_electronico,
         fecha_contratacion, salario, activo)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
        RETURNING id_empleado INTO :8
    """
    conn = None
    cursor = None

    try:
        print("[PRUEBA 1] Conectando a Oracle...")
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            print("[PRUEBA 2] Conexión establecida.")

            direccion_cifrada = cifrar_dato(empleado.direccion)
            telefono_cifrado = cifrar_dato(empleado.telefono)

            id_generado = cursor.var(oracledb.NUMBER)

            print("[PRUEBA 3] Ejecutando INSERT...")

            cursor.execute(
                consulta_insert,
                (
                    empleado.nombre,
                    direccion_cifrada,
                    telefono_cifrado,
                    empleado.correo_electronico,
                    empleado.fecha_contratacion,
                    empleado.salario,
                    int(empleado.activo),
                    id_generado
                )
            )

            print("[PRUEBA 4] INSERT ejecutado correctamente.")

            valor_id = id_generado.getvalue()

            print("[DEBUG] Valor recibido:", valor_id)
            print("[DEBUG] Tipo recibido:", type(valor_id))

            while isinstance(valor_id, list):
                valor_id = valor_id[0]
                
            empleado.id_empleado = int(valor_id)
            
            print("[DEBUG] ID convertido:", empleado.id_empleado)

            print(f"[PRUEBA 5] ID generado: {empleado.id_empleado}")

            conn.commit()
            print("[INFO] Empleado registrado correctamente.")

    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Empleado no registrado: {e}")
        import traceback
        traceback.print_exc()

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
        RETURNING id_empleado INTO :8
    """

    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()

            direccion_cifrada = cifrar_dato(empleado.direccion) #CIFRAR LOS DATOS PERSONALES ANTES DE GUARDARLOS CON FERNET
            telefono_cifrado = cifrar_dato(empleado.telefono)

            id_generado = cursor.var(oracledb.NUMBER)
            
            cursor.execute(
                consulta_insert,
                (
                    empleado.nombre,
                    direccion_cifrada, #DATOS CIFRADOS
                    telefono_cifrado,
                    empleado.correo_electronico,
                    empleado.fecha_contratacion,
                    empleado.salario,
                    int(empleado.activo),
                    id_generado
                )
            )

            valor_id = id_generado.getvalue()

            print("[DEBUG] Valor recibido:", repr(valor_id))
            print("[DEBUG] Tipo recibido:", type(valor_id))

            while isinstance(valor_id, list):
                valor_id = valor_id[0]
            
            print("[DEBUG] Valor final:", repr(valor_id))
            
            empleado.id_empleado = int(valor_id)

            conn.commit()
            print(f"[INFO] Empleado registrado correctamente. ID: {empleado.id_empleado}")

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

def obtener_empleado_por_id(id_empleado: int):

    consulta_sql = """
        SELECT
            id_empleado,
            nombre,
            direccion,
            telefono,
            correo_electronico,
            fecha_contratacion,
            salario,
            activo
        FROM empleados
        WHERE id_empleado = :1
    """

    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql, (id_empleado,))

            resultado = cursor.fetchone()

            if resultado:
                empleado = Empleado(
                    nombre=resultado[1],
                    direccion=resultado[2],
                    telefono=resultado[3],
                    correo_electronico=resultado[4],
                    fecha_contratacion=resultado[5],
                    salario=resultado[6]
                )

                empleado.id_empleado = resultado[0]
                empleado.activo = bool(resultado[7])

                return empleado

            print("[WARNING] Empleado no encontrado.")
            return None

    except Exception as e:
        print(f"[ERROR] No se pudo consultar el empleado | {e}")
        return None

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

        direccion = descifrar_dato(self.direccion) #DESCIFRAR LOS DATOS PERSONALES ANTES DE MOSTRARLOS
        telefono = descifrar_dato(self.telefono)


        return (
            f"Empleado\n"
            f"ID: {self.id_empleado}\n"
            f"Nombre: {self.nombre}\n"
            f"Dirección: {direccion}\n"
            f"Teléfono: {telefono}\n"
            f"Correo: {self.correo_electronico}\n"
            f"Fecha contratación: {self.fecha_contratacion}\n"
            f"Salario: {self.salario}\n"
            f"Activo: {self.activo}"
        )