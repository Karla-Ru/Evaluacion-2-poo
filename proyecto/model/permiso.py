from config.app_config import conectar_db, oracledb

#CREAR TABLA PERMISOS

def validar_tabla_permiso():

    consulta_sql = """
        CREATE TABLE permisos (
            id_permiso NUMBER GENERATED ALWAYS AS IDENTITY
                (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(80) NOT NULL,
            descripcion VARCHAR2(250),

            CONSTRAINT uq_permiso_nombre UNIQUE (nombre)
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
        print("Tabla permisos verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print("Error al crear la tabla permisos:", e)

    finally:
        cursor.close()
        conn.close()

#INSERTAR PERMISO

def insertar_permiso(permiso):

    consulta_sql = """
        INSERT INTO permisos (nombre, descripcion)
        VALUES (:1, :2)
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            consulta_sql,
            (
                permiso.nombre,
                permiso.descripcion
            )
        )

        conn.commit()
        print("Permiso registrado correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error: el permiso ya existe.", e)

    except Exception as e:
        conn.rollback()
        print("Error al registrar el permiso:", e)

    finally:
        cursor.close()
        conn.close()

#REPOSITORIO PERMISO

class PermisoRepositorio:

    def __init__(self):
        pass

    def actualizar_descripcion(self, nueva_descripcion: str):

        consulta_sql = """
            UPDATE permisos
            SET descripcion = :1
            WHERE id_permiso = :2
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (nueva_descripcion, self.id_permiso)
            )

            conn.commit()

            if cursor.rowcount > 0:
                self.descripcion = nueva_descripcion
                print("Descripción del permiso actualizada.")
            else:
                print("No se encontró el permiso.")

        except Exception as e:
            conn.rollback()
            print("Error al actualizar el permiso:", e)

        finally:
            cursor.close()
            conn.close()

    def eliminar_permiso(self):

        consulta_sql = """
            DELETE FROM permisos
            WHERE id_permiso = :1
        """

        conn = conectar_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                consulta_sql,
                (self.id_permiso,)
            )

            conn.commit()

            if cursor.rowcount > 0:
                print("Permiso eliminado correctamente.")
            else:
                print("No se encontró el permiso.")

        except oracledb.IntegrityError:
            conn.rollback()
            print(
                "No se puede eliminar el permiso porque "
                "está asociado a uno o más roles."
            )

        except Exception as e:
            conn.rollback()
            print("Error al eliminar el permiso:", e)

        finally:
            cursor.close()
            conn.close()

#CLASE PERMISO

class Permiso(PermisoRepositorio):

    def __init__(
        self,
        nombre: str,
        descripcion: str
    ):

        super().__init__()

        self.id_permiso = None
        self.nombre = nombre
        self.descripcion = descripcion

    def mostrar_datos(self):

        return (
            f"ID Permiso: {self.id_permiso}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}"
        )
