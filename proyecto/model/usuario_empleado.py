from usuario_sistema import UsuarioSistema
from config.app_config import conectar_db, oracledb


# ==========================================
# INSERTAR USUARIO EMPLEADO
# ==========================================

def insertar_usuario_empleado(usuario):

    consulta_sql = """
        INSERT INTO usuarios_sistema
        (nombre_usuario, clave_hash, tipo_usuario, activo, id_empleado)
        VALUES (:1, :2, :3, :4, :5)
    """

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            consulta_sql,
            (
                usuario.nombre_usuario,
                usuario.clave_hash,
                usuario.obtener_tipo_usuario(),
                1,
                usuario.id_empleado
            )
        )

        conn.commit()
        print("Usuario empleado registrado correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error: el nombre de usuario o el empleado ya está registrado.", e)

    except Exception as e:
        conn.rollback()
        print("Error al registrar el usuario empleado:", e)

    finally:
        cursor.close()
        conn.close()


# ==========================================
# CLASE USUARIO EMPLEADO
# ==========================================

class UsuarioEmpleado(UsuarioSistema):

    def __init__(
        self,
        nombre_usuario: str,
        clave: str,
        id_empleado: int
    ):

        super().__init__(nombre_usuario, clave)

        self.id_empleado = id_empleado

    def obtener_tipo_usuario(self):

        return "EMPLEADO"

    def mostrar_datos(self):

        return (
            super().mostrar_datos()
            + f"\nID Empleado asociado: {self.id_empleado}"
        )