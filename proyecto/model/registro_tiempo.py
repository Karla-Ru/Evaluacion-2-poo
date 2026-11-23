from datetime import date
from proyecto.config.app_config import conectar_db, oracledb
from proyecto.model.asignacion_proyecto import esta_asignado, ejecutar_cambio_bd, consultar_bd

def validar_tabla_registro_tiempo():
    consulta_sql = """
        create table registros_tiempo (
            id_registro NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            id_empleado NUMBER NOT NULL,
            id_proyecto NUMBER NOT NULL,
            fecha DATE NOT NULL,
            horas_trabajadas NUMBER(4,1) NOT NULL,
            descripcion VARCHAR2(300),
            CONSTRAINT ck_registro_horas CHECK (horas_trabajadas > 0 and horas_trabajadas <= 24),
            CONSTRAINT fk_registro_empleado FOREIGN KEY (id_empleado)
                REFERENCES empleados(id_empleado),
            CONSTRAINT fk_registro_proyecto FOREIGN KEY (id_proyecto)
                REFERENCES proyectos(id_proyecto) ON  delete cascade
        )
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("Tabla registros_tiempo creada correctamente")
    except oracledb.DatabaseError as e:
        error = e.args[0]

        if error.code == 955: #La tabla ya existe
            print("registros_tiempo verificada correctamente")
        else:
            print(f"Error: Creación de tabla registros_tiempo | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def horas_validas(horas) -> bool:
    if not isinstance(horas, (int, float)) or horas <= 0 or horas >24:
        print("[ERROR] Las horas trabajadas deben ser un número entre 0 y 24")
        return False
    return True

def insertar_datos_registro(registro):
    consulta_insert = """
        insert into registros_tiempo (id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion)
        values (:1, :2, :3, :4, :5)
        returning id_registro into :6
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            id_generado = cursor.var(oracledb.NUMBER) 
            cursor.execute(consulta_insert, (registro.id_empleado, registro.id_proyecto, registro.fecha, registro.horas_trabajadas, registro.descripcion, id_generado))
            conn.commit()

            registro.id_registro = int(id_generado.getvalue()[0])
            print(f"Se registraron {registro.horas_trabajadas} horas trabajadas (registro {registro.id_registro})")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"Registro de tiempo no guardado | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def obtener_registro(id_registro: int):
    filas = consultar_bd("""
        select id_registro, id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion
        from registros_tiempo
        where id_registro = :1
    """, (id_registro,))
    return filas[0] if filas else None

def listar_registros_proyecto(id_proyecto: int) -> list:
    return consultar_bd("""
        select id_registro, id_empleado, fecha, horas_trabajadas, descripcion
        from registros_tiempo
        where id_proyecto = :1
        order by fecha, id_registro
    """, (id_proyecto,))


def listar_registros_empleado(id_empleado: int) -> list:
    return consultar_bd( """
        SELECT id_registro, id_proyecto, fecha, horas_trabajadas, descripcion
        FROM registros_tiempo
        WHERE id_empleado = :1
        ORDER BY fecha, id_registro
""", (id_empleado,))

def total_horas_proyecto(id_proyecto: int) -> float:
    filas = consultar_bd("select nvl(sum(horas_trabajadas), 0) from registros_tiempo where id_proyecto = :1", (id_proyecto,))
    return float(filas[0][0]) if filas else 0.0

def total_horas_empleado(id_empleado: int) -> float:
    filas = consultar_bd("select nvl(sum(horas_trabajadas), 0) from registros_tiempo where id_empleado = :1", (id_empleado,))
    return float(filas[0][0]) if filas else 0.0


class RegistroTiempoRepositorio():
    def __init__(self):
        pass

    def modificar_registro(self, horas_trabajadas: float = None, descripcion: str = None):
        nuevas_horas      = horas_trabajadas if horas_trabajadas is not None else self.horas_trabajadas
        nueva_descripcion = descripcion if descripcion is not None else self.descripcion

        if not horas_validas(nuevas_horas): 
            return False

        actualizado = ejecutar_cambio_bd(
            "update registros_tiempo set horas_trabajadas = :1, descripcion = :2 where id_registro = :3",
            (nuevas_horas, nueva_descripcion, self.id_registro)
        )

        if actualizado:
            self.horas_trabajadas = nuevas_horas
            self.descripcion      = nueva_descripcion
            print("Registro de tiempo actualizado correctamente.")
        else:
            print("No se pudo actualizar el registro tiempo")
        return actualizado

    def eliminar_registro(self):
        eliminado = ejecutar_cambio_bd("delete from registros_tiempo where id_registro = :1", (self.id_registro,))
        if eliminado:
            print("Registro de tiempo eliminado")
            self.id_registro = None
        else:
            print("Registro de tiempo no encontrado")
        return eliminado


class RegistroTiempo(RegistroTiempoRepositorio):
    def __init__(self, id_empleado: int, id_proyecto: int, horas_trabajadas: float, descripcion: str = "", fecha: date = None):
        self.id_registro      = None  # Lo asigna Oracle
        self.id_empleado      = id_empleado
        self.id_proyecto      = id_proyecto
        self.fecha            = fecha or date.today()
        self.horas_trabajadas = horas_trabajadas
        self.descripcion      = descripcion
        self.registrar_horas()

    def registrar_horas(self):
        if not horas_validas(self.horas_trabajadas):
            return False

        if self.fecha > date.today():
            print("No se pueden registrar horas en una fecha futura")
            return False

        validar_tabla_registro_tiempo()

        if not esta_asignado(self.id_empleado, self.id_proyecto):
            print(f"El empleado {self.id_empleado} no está asignado al proyecto {self.id_proyecto}")
            return False

        insertar_datos_registro(self)
        return self.id_registro is not None

    def mostrar_datos(self):
        return (f"Registro de Tiempo\n ID: {self.id_registro} | Fecha: {self.fecha} | "
                f"Empleado: {self.id_empleado} | Proyecto: {self.id_proyecto} | "
                f"Horas: {self.horas_trabajadas} | Descripción: {self.descripcion}")