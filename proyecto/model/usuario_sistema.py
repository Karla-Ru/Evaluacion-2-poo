
from abc import ABC, abstractmethod

from proyecto.config.app_config import conectar_db
from proyecto.security.seguridad_contraseñas import (
    generar_hash,
    verificar_hash,
    necesita_actualizacion
)

#CONFIGURACIÓN DEL BLOQUEO
MAX_INTENTOS = 3
MINUTOS_BLOQUEO = 15

#CREAR Y ACTUALIZAR TABLA DE USUARIOS

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
            intentos_fallidos NUMBER(1) DEFAULT 0 NOT NULL,
            bloqueado_hasta TIMESTAMP,

            CONSTRAINT uq_usuario_nombre UNIQUE (nombre_usuario),
            CONSTRAINT uq_usuario_empleado UNIQUE (id_empleado),
            CONSTRAINT chk_usuario_activo CHECK (activo IN (0, 1)),
            CONSTRAINT chk_intentos_fallidos
                CHECK (intentos_fallidos BETWEEN 0 AND 3),
            CONSTRAINT fk_usuario_empleado
                FOREIGN KEY (id_empleado)
                REFERENCES empleados(id_empleado)
        )
    """

    conn = conectar_db()

    if conn is None:
        print("[ERROR] No se pudo conectar a Oracle.")
        return

    cursor = conn.cursor()

    try:
        #CREAR TABLA SI AÚN NO EXISTE
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

        #AGREGAR COLUMNAS A INSTALACIONES ANTERIORES
        #ORA-01430 SIGNIFICA QUE LA COLUMNA YA EXISTE

        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE
                    'ALTER TABLE usuarios_sistema
                     ADD (intentos_fallidos NUMBER(1)
                     DEFAULT 0 NOT NULL)';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -1430 THEN
                        RAISE;
                    END IF;
            END;
        """)

        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE
                    'ALTER TABLE usuarios_sistema
                     ADD (bloqueado_hasta TIMESTAMP)';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -1430 THEN
                        RAISE;
                    END IF;
            END;
        """)

        conn.commit()

        print("[INFO] Tabla usuarios_sistema verificada correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] No se pudo verificar la tabla: {e}")

    finally:
        cursor.close()
        conn.close()

#CLASE PADRE USUARIO SISTEMA
class UsuarioSistema(ABC):

    def __init__(self, nombre_usuario: str, clave: str):

        self.id_usuario = None
        self.nombre_usuario = nombre_usuario

        # Nuevas contraseñas: Argon2id
        self.clave_hash = generar_hash(clave)

        self.activo = True

    @abstractmethod
    def obtener_tipo_usuario(self):
        pass

    def verificar_clave(self, clave_ingresada: str):

        return verificar_hash(
            clave_ingresada,
            self.clave_hash
        )

    def mostrar_datos(self):

        return (
            f"ID Usuario: {self.id_usuario}\n"
            f"Nombre de usuario: {self.nombre_usuario}\n"
            f"Tipo de usuario: {self.obtener_tipo_usuario()}\n"
            f"Estado: {'Activo' if self.activo else 'Inactivo'}"
        )

#AUTENTICACIÓN Y CONTROL DE INTENTOS

def autenticar_usuario(nombre_usuario: str, clave: str):

    consulta_sql = """
        SELECT id_usuario,
               nombre_usuario,
               clave_hash,
               tipo_usuario,
               activo,
               intentos_fallidos,
               CASE
                   WHEN bloqueado_hasta > SYSTIMESTAMP THEN 1
                   ELSE 0
               END AS esta_bloqueado
        FROM usuarios_sistema
        WHERE nombre_usuario = :1
        FOR UPDATE
    """

    conn = conectar_db()

    if conn is None:
        print("[ERROR] No se pudo conectar a Oracle.")
        return False

    cursor = conn.cursor()

    try:

        #BLOQUEAR LA FILA MIENTRAS SE ACTUALIZAN LOS INTENTOS
        cursor.execute(consulta_sql, (nombre_usuario,))
        resultado = cursor.fetchone()

        if resultado is None:
            conn.rollback()
            print("[ERROR] Usuario o contraseña incorrectos.")
            return False

        (
            id_usuario,
            nombre,
            clave_hash,
            tipo,
            activo,
            intentos,
            esta_bloqueado
        ) = resultado

        if activo != 1:
            conn.rollback()
            print("[ERROR] La cuenta se encuentra desactivada.")
            return False

        #COMPROBAR BLOQUEO VIGENTE
        if esta_bloqueado == 1:
            conn.rollback()
            print("[ERROR] La cuenta está bloqueada temporalmente.")
            print("[INFO] Intente nuevamente después de 15 minutos.")
            return False

        #SI EL BLOQUEO ANTERIOR YA VENCIÓ. REINICIAR CONTADOR
        if intentos >= MAX_INTENTOS:

            cursor.execute("""
                UPDATE usuarios_sistema
                SET intentos_fallidos = 0,
                    bloqueado_hasta = NULL
                WHERE id_usuario = :1
            """, (id_usuario,))

            intentos = 0

        #COMPROBAR CONTRASEÑA
        clave_valida = verificar_hash(clave, clave_hash)

        if clave_valida:

            #MIGRAR HASHES BCRYPT ANTIGUOS A ARGON2ID
            if necesita_actualizacion(clave_hash):

                nuevo_hash = generar_hash(clave)

                cursor.execute("""
                    UPDATE usuarios_sistema
                    SET clave_hash = :1
                    WHERE id_usuario = :2
                """, (nuevo_hash, id_usuario))

            #RESTABLECER INTENTOS DESPUÉS DEL ACCESO CORRECTO 
            cursor.execute("""
                UPDATE usuarios_sistema
                SET intentos_fallidos = 0,
                    bloqueado_hasta = NULL
                WHERE id_usuario = :1
            """, (id_usuario,))

            conn.commit()

            print("[INFO] Inicio de sesión exitoso.")
            print(f"[INFO] Tipo de usuario: {tipo}")

            return True

        #CONTRASEÑA INCORRECTA: INCREMENTAR CONTADOR
        nuevos_intentos = intentos + 1

        if nuevos_intentos >= MAX_INTENTOS:

            cursor.execute("""
                UPDATE usuarios_sistema
                SET intentos_fallidos = :1,
                    bloqueado_hasta =
                        SYSTIMESTAMP + INTERVAL '15' MINUTE
                WHERE id_usuario = :2
            """, (MAX_INTENTOS, id_usuario))

            conn.commit()

            print("[ERROR] Se alcanzó el límite de intentos.")
            print("[ERROR] Cuenta bloqueada durante 15 minutos.")

            return False

        cursor.execute("""
            UPDATE usuarios_sistema
            SET intentos_fallidos = :1
            WHERE id_usuario = :2
        """, (nuevos_intentos, id_usuario))

        conn.commit()

        restantes = MAX_INTENTOS - nuevos_intentos

        print("[ERROR] Usuario o contraseña incorrectos.")
        print(f"[WARNING] Intentos restantes: {restantes}")

        return False

    except Exception as e:

        conn.rollback()
        print(f"[ERROR] Error durante la autenticación: {e}")

        return False

    finally:
        cursor.close()
        conn.close()