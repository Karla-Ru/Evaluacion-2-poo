from config.app_config import conectar_db, oracledb

from proyecto.model.permiso import Permiso

#CREAR TABLA ROLES

def validar_tabla_rol():

    consulta_sql = """
        CREATE TABLE roles (
            id_rol NUMBER GENERATED ALWAYS AS IDENTITY
                (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(50) NOT NULL,
            descripcion VARCHAR2(250),

            CONSTRAINT uq_rol_nombre UNIQUE (nombre)
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
        print("Tabla roles verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print("Error al crear la tabla roles:", e)

    finally:
        cursor.close()
        conn.close()

#CREAR TABLA INTERMEDIA ROL_PERMISO

def validar_tabla_rol_permiso():

    consulta_sql = """
        CREATE TABLE rol_permiso (
            id_rol NUMBER NOT NULL,
            id_permiso NUMBER NOT NULL,

            CONSTRAINT pk_rol_permiso
                PRIMARY KEY (id_rol, id_permiso),

            CONSTRAINT fk_rp_rol
                FOREIGN KEY (id_rol)
                REFERENCES roles(id_rol),

            CONSTRAINT fk_rp_permiso
                FOREIGN KEY (id_permiso)
                REFERENCES permisos(id_permiso)
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
        print("Tabla rol_permiso verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print("Error al crear la tabla rol_permiso:", e)

    finally:
        cursor.close()
        conn.close()

#INSERTAR ROL

def insertar_rol(rol):

    consulta_sql = """
        INSERT INTO roles (nombre, descripcion)
        VALUES (:1, :2)
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            consulta_sql,
            (rol.nombre, rol.descripcion)
        )

        conn.commit()
        print("Rol registrado correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error: el rol ya existe o los datos no son válidos.", e)

    except Exception as e:
        conn.rollback()
        print("Error al registrar el rol:", e)

    finally:
        cursor.close()
        conn.close()

#ASIGNAR PERMISO A UN ROL

def asignar_permiso_rol(id_rol: int, id_permiso: int):

    consulta_sql = """
        INSERT INTO rol_permiso (id_rol, id_permiso)
        VALUES (:1, :2)
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            consulta_sql,
            (id_rol, id_permiso)
        )

        conn.commit()
        print("Permiso asignado al rol correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error: el rol o permiso no existe, o ya están relacionados.", e)

    except Exception as e:
        conn.rollback()
        print("Error al asignar permiso:", e)

    finally:
        cursor.close()
        conn.close()

#CLASE ROL
class Rol:

    def __init__(
        self,
        nombre: str,
        descripcion: str
    ):

        self.id_rol = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.permisos = []

    def agregar_permiso(self, permiso):

        if permiso not in self.permisos:
            self.permisos.append(permiso)

    def mostrar_permisos(self):

        return [
            permiso.nombre for permiso in self.permisos
        ]

    def mostrar_datos(self):

        return (
            f"ID Rol: {self.id_rol}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Permisos: {', '.join(self.mostrar_permisos())}"
        )

#CLASE PERMISO (SE ELIMINA CLASE PERMISO)
#(SE ELIMINA CREAR TABLA PERMISOS)
# SE ELIMINA INSERTAR PERMISO
# SE ELIMINA CREAR TABLA INTERMEDIA ROL_PERMISO (VALIDAR)