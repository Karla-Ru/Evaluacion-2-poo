from datetime import date
from proyecto.config.app_config import conectar_db, oracledb
from proyecto.model.asignacion_proyecto import (AsignacionProyecto, eliminar_asignacion_bd, ejecutar_cambio_bd, consultar_bd)

def validar_tabla_proyecto():

    consultas_sql = """
        CREATE TABLE proyectos (
            id_proyecto NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(100) NOT NULL,
            descripcion VARCHAR2(300),
            fecha_inicio DATE NOT NULL,
            fecha_termino DATE NOT NULL,
            estado VARCHAR2(20) DEFAULT 'Pendiente' NOT NULL,
            CONSTRAINT uq_proyecto_nombre UNIQUE (nombre),
            CONSTRAINT ck_proyecto_fechas CHECK (fecha_termino >= fecha_inicio),
            CONSTRAINT ck_proyecto_estado CHECK (estado IN ('Pendiente','En curso','Finalizado','Cancelado'))
        )
        """

    conn = None
    cursor = None

    try:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(consultas_sql)
            print("Tabla proyecto creada correctamente")
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 955: #Ya existe
             print("Tabla proyectos verificada correctamente")
        else:
             print(f"Error al validar tablas de proyecto: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def obtener_id_proyecto(nombre: str):
    filas = consultar_bd("select id_proyecto from proyectos where nombre = :1", (nombre,))
    return int(filas[0][0]) if filas else None


def insertar_datos_proyecto(proyecto):
    consulta_insert = """
        insert into proyectos (nombre, descripcion, fecha_inicio, fecha_termino, estado)
        values (:1, :2, :3, :4, :5)
        returning id_proyecto into :6
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            id_generado = cursor.var(oracledb.NUMBER)  #Oracle devuelve el id creado
            cursor.execute(consulta_insert, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio,
                                             proyecto.fecha_termino, proyecto.estado, id_generado))
            conn.commit()

            proyecto.id_proyecto = int(id_generado.getvalue()[0])
            print(f"[INFO] Proyecto insertado correctamente (ID {proyecto.id_proyecto})")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()  

        error = e.args[0]

        if error.code == 1:  # Existe un proyecto con ese nombre 
            print("[WARNING] Ya existe un proyecto con ese nombre")
            proyecto.id_proyecto = obtener_id_proyecto(proyecto.nombre)
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Proyecto no registrado | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def obtener_proyecto(id_proyecto: int):
    filas = consultar_bd("""
        select id_proyecto, nombre, descripcion, fecha_inicio, fecha_termino, estado 
        from proyectos
        where id_proyecto = :1
    """, (id_proyecto))
    return filas[0] if filas else None

# Retorna como lista de tuplas
def listar_proyectos() -> list:
    return consultar_bd("""
        select id_proyecto, nombre, estado, fecha_inicio, fecha_termino
        from proyectos
        order by id_proyecto
    """, ())

class ProyectoRepositorio():
    def __init__(self):
        pass

    def _ejecutar(self, consulta_sql: str, parametros: dict) -> bool:
        conn = None
        cursor = None
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(consulta_sql, parametros)
                conn.commit()
                return cursor.rowcount > 0
            return False
        except oracledb.DatabaseError as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Base de datos | {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def modificarProyecto(self, nombre: str = None, descripcion: str = None, fechaInicio: date = None, fechaTermino: date = None):
        nuevo_nombre = nombre if nombre is not None else self.nombre
        nueva_descripcion = descripcion if descripcion is not None else self.descripcion
        nueva_fecha_inicio = fechaInicio if fechaInicio is not None else self.fecha_inicio
        nueva_fecha_termino = fechaTermino if fechaTermino is not None else self.fecha_termino

        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            print("Nombre no corresponde a tipo str o está vacío")
            return False

        if nueva_fecha_termino < nueva_fecha_inicio:
            print("La fecha de término no puede ser anterior a la de inicio")
            return False

        actualizado = ejecutar_cambio_bd("""
            update proyectos set nombre = :1, descripcion = :2, fecha_inicio = :3, fecha_termino = :4
            where id_proyecto = :5
        """, (nuevo_nombre, nueva_descripcion, nueva_fecha_inicio, nueva_fecha_termino, self.id_proyecto))

        if actualizado:
            self.nombre        = nuevo_nombre
            self.descripcion   = nueva_descripcion
            self.fecha_inicio  = nueva_fecha_inicio
            self.fecha_termino = nueva_fecha_termino
            print("[INFO] Proyecto actualizado correctamente")
        else:
            print("[ERROR] No se pudo actualizar el proyecto")
        return actualizado

    # Elimina el proyecto lo marca como cancelado y libera a los empleados
    def eliminarProyecto(self) -> bool:
        ok = self._ejecutar(
            "DELETE FROM proyectos WHERE id_proyecto = :id_proyecto",
            {"id_proyecto": self.id_proyecto},
        )
        print(f"Proyecto '{self.nombre}' eliminado." if ok else "No se encontró el proyecto a eliminar.")
        return ok

    def cambiar_estado(self, nuevo_estado: str):
        if not isinstance(nuevo_estado, str):
            print("Nuevo estado no corresponde a tipo str")
            return False

        if nuevo_estado not in self.estados_validos:
            print(f"Estado inválido. Use uno de: {', '.join(self.estados_validos)}")
            return False

        actualizado = ejecutar_cambio_bd("update proyectos set estado = :1 where id_proyecto = :2", (nuevo_estado, self.id_proyecto))

        if actualizado:
            self.estado = nuevo_estado
            print(f"[INFO] Estado del proyecto cambiado a '{nuevo_estado}'")
        else:
            print("[ERROR] No se pudo cambiar el estado")
        return actualizado
class Proyecto(ProyectoRepositorio):
    estados_validos = ("Pendiente", "En curso", "Finalizado", "Cancelado")

    def __init__(self, nombre: str, descripcion: str, fechaInicio: date, fechaTermino: date, estado: str = "Pendiente"):
        self.id_proyecto   = None 
        self.nombre        = nombre
        self.descripcion   = descripcion
        self.fecha_inicio  = fechaInicio
        self.fecha_termino = fechaTermino
        self.estado        = estado or "Pendiente"
        
        self.crearProyecto ()

    # Validar datos del proyecto antes de crearlo
    def crearProyecto(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            print("Error: El nombre del proyecto no puede estar vacío.")
            return False
        if self.fecha_termino < self.fecha_inicio:
            print("Error: La fecha de término no puede ser anterior a la de inicio.")
            return False
        if self.estado not in self.estados_validos:
            print(f"Error: Estado inválido. Use uno de: {', '.join(self.estados_validos)}")
            return False

        validar_tabla_proyecto()
        insertar_datos_proyecto(self)
        return self.id_proyecto is not None


    def asignarEmpleado(self, id_empleado: int, rol_en_proyecto: str, horas_asignadas: float):
        if self.id_proyecto is None:
            print(f"Error: El proyecto no está guardado en la base de datos.")
            return None

        return AsignacionProyecto(id_empleado, self.id_proyecto, rol_en_proyecto, horas_asignadas)

    def desasignarEmpleado(self, id_empleado: int) -> bool:
        return eliminar_asignacion_bd(id_empleado, self.id_proyecto)
    

    def mostrar_datos(self):
        return (f"Proyecto\n ID: {self.id_proyecto} | Nombre: {self.nombre} | Estado: {self.estado} | "
                f"Inicio: {self.fecha_inicio} | Término: {self.fecha_termino}")