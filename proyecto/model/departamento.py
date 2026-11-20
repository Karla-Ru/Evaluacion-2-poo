from config.app_config import conectar_db, oracledb

#Coso de departamento

def validar_tabla_departamento():

    consulta_sql = """
        CREATE TABLE departamentos (
            id_departamento NUMBER GENERATED ALWAYS AS IDENTITY
                (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(100) NOT NULL,
            descripcion VARCHAR2(250),
            id_gerente NUMBER,

            CONSTRAINT uq_departamento_nombre UNIQUE (nombre),

            CONSTRAINT fk_departamento_gerente
                FOREIGN KEY (id_gerente)
                REFERENCES empleados(id_empleado)
        )
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
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

        conn.commit()
        print("Tabla departamentos verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print("Error al crear la tabla departamentos:", e)

    finally:
        cursor.close()
        conn.close()

def insertar_datos_departamento(departamento):

    consulta_insert = """
        INSERT INTO departamentos
        (nombre, descripcion, id_gerente)
        VALUES (:1, :2, :3)
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            consulta_insert,
            (
                departamento.nombre,
                departamento.descripcion,
                departamento.id_gerente
            )
        )

        conn.commit()
        print("Departamento registrado correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error de integridad al registrar el departamento:", e)

    except Exception as e:
        conn.rollback()
        print("Error al registrar el departamento:", e)

    finally:
        cursor.close()
        conn.close()

class DepartamentoRepositorio:

    def __init__(self):
        pass

    def actualizar_nombre(self, nuevo_nombre: str):

        consulta_sql = """
            UPDATE departamentos
            SET nombre = :1
            WHERE id_departamento = :2
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (nuevo_nombre, self.id_departamento)
            )

            conn.commit()

            if cursor.rowcount > 0:
                self.nombre = nuevo_nombre
                print("Nombre del departamento actualizado.")
            else:
                print("No se encontró el departamento.")

        except Exception as e:
            conn.rollback()
            print("Error al actualizar el nombre:", e)

        finally:
            cursor.close()
            conn.close()

    def actualizar_descripcion(self, nueva_descripcion: str):

        consulta_sql = """
            UPDATE departamentos
            SET descripcion = :1
            WHERE id_departamento = :2
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (nueva_descripcion, self.id_departamento)
            )

            conn.commit()

            if cursor.rowcount > 0:
                self.descripcion = nueva_descripcion
                print("Descripción actualizada correctamente.")
            else:
                print("No se encontró el departamento.")

        except Exception as e:
            conn.rollback()
            print("Error al actualizar la descripción:", e)

        finally:
            cursor.close()
            conn.close()

    def asignar_gerente(self, id_gerente: int):

        consulta_sql = """
            UPDATE departamentos
            SET id_gerente = :1
            WHERE id_departamento = :2
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (id_gerente, self.id_departamento)
            )

            conn.commit()

            if cursor.rowcount > 0:
                self.id_gerente = id_gerente
                print("Gerente asignado correctamente.")
            else:
                print("No se encontró el departamento.")

        except oracledb.IntegrityError:
            conn.rollback()
            print("El empleado indicado no existe.")

        except Exception as e:
            conn.rollback()
            print("Error al asignar gerente:", e)

        finally:
            cursor.close()
            conn.close()

    def eliminar_departamento(self):

        consulta_sql = """
            DELETE FROM departamentos
            WHERE id_departamento = :1
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (self.id_departamento,)
            )

            conn.commit()

            if cursor.rowcount > 0:
                print("Departamento eliminado correctamente.")
            else:
                print("No se encontró el departamento.")

        except oracledb.IntegrityError:
            conn.rollback()
            print("No se puede eliminar: existen registros relacionados.")

        except Exception as e:
            conn.rollback()
            print("Error al eliminar el departamento:", e)

        finally:
            cursor.close()
            conn.close()

class Departamento(DepartamentoRepositorio):

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        id_gerente: int = None
    ):

        super().__init__()

        self.id_departamento = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_gerente = id_gerente

    def mostrar_datos(self):

        return (
            f"ID Departamento: {self.id_departamento}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"ID Gerente: {self.id_gerente}"
        )