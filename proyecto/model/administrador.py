from proyecto.model.usuario_sistema import UsuarioSistema
from proyecto.config.app_config import conectar_db, oracledb

#INSERTAR ADMINISTRADOR

def insertar_administrador(administrador):

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
                administrador.nombre_usuario,
                administrador.clave_hash,
                administrador.obtener_tipo_usuario(),
                1,
                None
            )
        )

        conn.commit()
        print("Administrador registrado correctamente.")

    except oracledb.IntegrityError as e:
        conn.rollback()
        print("Error: el nombre de usuario ya existe.", e)

    except Exception as e:
        conn.rollback()
        print("Error al registrar administrador:", e)

    finally:
        cursor.close()
        conn.close()

#CLASE ADMINISTRADOR

class Administrador(UsuarioSistema):

    def __init__(
        self,
        nombre_usuario: str,
        clave: str
    ):

        super().__init__(nombre_usuario, clave)

        self.permisos = [
            "GESTIONAR_EMPLEADOS",
            "GESTIONAR_DEPARTAMENTOS",
            "GESTIONAR_PROYECTOS",
            "GESTIONAR_REGISTROS_TIEMPO",
            "GESTIONAR_USUARIOS",
            "CONSULTAR_INFORMES"
        ]

    def obtener_tipo_usuario(self):

        return "ADMINISTRADOR"

    def gestionar_empleados(self):

        print("El administrador puede gestionar empleados.")

    def gestionar_departamentos(self):

        print("El administrador puede gestionar departamentos.")

    def gestionar_proyectos(self):

        print("El administrador puede gestionar proyectos.")

    def gestionar_usuarios(self):

        print("El administrador puede gestionar las cuentas del sistema.")

    def consultar_informes(self):

        print("El administrador puede consultar los informes del sistema.")

    def mostrar_permisos(self):

        return self.permisos

    def mostrar_datos(self):

        return (
            super().mostrar_datos()
            + "\nPermisos: " + ", ".join(self.permisos)
        )