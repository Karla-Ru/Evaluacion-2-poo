from abc import ABC, abstractmethod
from config.app_config import conectar_db, oracledb
import bcrypt


# ==========================================
# CREAR TABLA USUARIOS DEL SISTEMA
# ==========================================

def validar_tabla_usuario_sistema():

    consulta_sql = """
        CREATE TABLE usuarios_sistema (
        id_usuario NUMBER GENERATED ALWAYS AS IDENTITY
        (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
        nombre_usuario VARCHAR2(50) NOT NULL,
        clave_hash VARCHAR2(255) NOT NULL,
        tipo_usuario VARCHAR2(30) NOT NULL,
        activo NUMBER(1) DEFAULT 1 NOT NULL,
        fecha_creacion DATE DEFAULT SYSDATE,
        id_empleado NUMBER,
        
        CONSTRAINT uq_usuario_nombre UNIQUE (nombre_usuario),
        CONSTRAINT uq_usuario_empleado UNIQUE (id_empleado),
        CONSTRAINT chk_usuario_activo CHECK (activo IN (0, 1)),
        CONSTRAINT fk_usuario_empleado
        FOREIGN KEY (id_empleado)
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
        print("Tabla usuarios_sistema verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print("Error al crear la tabla usuarios_sistema:", e)

    finally:
        cursor.close()
        conn.close()


# ==========================================
# CLASE PADRE USUARIO SISTEMA
# ==========================================

class UsuarioSistema(ABC):

    def __init__(
        self,
        nombre_usuario: str,
        clave: str
    ):

        self.id_usuario = None
        self.nombre_usuario = nombre_usuario

        # La contraseña se almacena como hash, no como texto plano.
        self.clave_hash = bcrypt.hashpw(
            clave.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        self.activo = True

    @abstractmethod
    def obtener_tipo_usuario(self):
        pass

    def verificar_clave(self, clave_ingresada: str):

        return bcrypt.checkpw(
            clave_ingresada.encode("utf-8"),
            self.clave_hash.encode("utf-8")
        )

    def mostrar_datos(self):

        return (
            f"ID Usuario: {self.id_usuario}\n"
            f"Nombre de usuario: {self.nombre_usuario}\n"
            f"Tipo de usuario: {self.obtener_tipo_usuario()}\n"
            f"Estado: {'Activo' if self.activo else 'Inactivo'}"
        )


# ==========================================
# AUTENTICAR USUARIO
# ==========================================

def autenticar_usuario(nombre_usuario: str, clave: str):

    consulta_sql = """
        SELECT id_usuario, nombre_usuario, clave_hash,
               tipo_usuario, activo
        FROM usuarios_sistema
        WHERE nombre_usuario = :1
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(consulta_sql, (nombre_usuario,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("El usuario no existe.")
            return False

        id_usuario, nombre, clave_hash, tipo, activo = resultado

        if activo != 1:
            print("La cuenta se encuentra desactivada.")
            return False

        clave_valida = bcrypt.checkpw(
            clave.encode("utf-8"),
            clave_hash.encode("utf-8")
        )

        if clave_valida:
            print("Inicio de sesión exitoso.")
            return True

        print("La contraseña es incorrecta.")
        return False

    except Exception as e:
        print("Error durante la autenticación:", e)
        return False

    finally:
        cursor.close()
        conn.close()