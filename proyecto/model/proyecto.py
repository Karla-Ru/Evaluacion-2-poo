from datetime import date
from proyecto.config.app_config import conectar_db, oracledb

def validar_tabla_proyecto():

    consultas_sql = [
        """
        CREATE TABLE proyectos (
            id_proyecto NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            nombre VARCHAR2(100) NOT NULL,
            descripcion VARCHAR2(300),
            fecha_Inicio DATE NOT NULL,
            fecha_Termino DATE NOT NULL,
            estado VARCHAR2(20) DEFAULT 'Pendiente' NOT NULL,
            CONSTRAINT ck_proyecto_fechas
                CHECK (fecha_termino >= fecha_inicio),
            CONSTRAINT ck_proyecto_estado
                CHECK (estado IN ('Pendiente','En curso','Finalizado','Cancelado'))
        )
        """,
        """
        CREATE TABLE proyecto_empleado (
        id_proyecto NUMBER NOT NULL,
        id_empleado NUMBER NOT NULL,
        CONSTRAINT pk_proyecto_empleado
            PRIMARY KEY (id_proyecto, id_empleado)
        CONSTRAINT fk_pe_proyecto
            FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
            ON DELETE CASCADE,
        COONSTRAINT fk_pe_empleado
            FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
        )
        """,
    ]

    conn = None
    cursor = None

    try:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            for consulta_sql in consulta_sql:
                try:
                    cursor.execute(consulta_sql)
                    print("Tabla creada correctamente")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    if error.code == 955: #El nombre ya está en uso
                        print("La tabla ya existe")
                    else:
                        raise
            conn.commit()

    except oracledb.DatabaseError as e:
        print(f"Error al validar tablas de proyecto: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

class Proyecto:
    """ Representa los proyectos desarrollados por la empresa """

    estados_validos = ("Pendiente", "En curso", "Finalizado", "Cancelado")

    def __init__(self, nombre: str, descripcion: str, fechaInicio: date, fechaTermino: date, estado: str = "Pendiente", idProyecto: int = None):
        self.__idProyecto   = idProyecto
        self.__nombre       = nombre
        self.__descripcion  = descripcion
        self.__fechaInicio  = fechaInicio
        self.__fechaTermino = fechaTermino
        self.__estado       = estado

    def idProyecto(self) -> int:
        return self.__idProyecto

    def nombre(self) -> str:
        return self.__nombre

    def nombre(self, valor: str):
        self.__nombre = valor

    def descripcion(self) -> str:
        return self.__descripcion

    def descripcion(self, valor: str):
        self.__descripcion = valor

    def fechaInicio(self) -> date:
        return self.__fechaInicio

    def fechaInicio(self, valor: date):
        self.__fechaInicio = valor

    def fechaTermino(self) -> date:
        return self.__fechaTermino

    def fechaTermino(self, valor: date):
        self.__fechaTermino = valor

    def estado(self) -> str:
        return self.__estado

# Ejecutar SQL
    @staticmethod
    def _ejecutar(consulta_sql: str, parametros: dict) -> bool:
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
            print(f"Error en la base de datos: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Validar datos del proyecto antes de crearlo
    def crearProyecto(self) -> bool:
        if not self.__nombre or not self.__nombre.strip():
            print("Error: El nombre del proyecto no puede estar vacío.")
            return False
        if self.__fechaTermino < self.__fechaInicio:
            print("Error: La fecha de término no puede ser anterior a la de inicio.")
            return False
        if self.__estado not in self.estados_validos:
            print(f"Error: Estado inválido. Use uno de: {', '.join(self.estados_validos)}")
            return False
        print(f"Proyecto '{self.__nombre}' creado correctamente")
        return True

        consulta_sql = """
        INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_termino, estado)
        VALUES (:nombre, :descripcion, :fecha:inicio, :fecha_termino, :estado)
        RETURNING id_proyecto INTO :id_proyecto
        """
        conn = None
        cursor = None
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                id_var = cursor.var(oracledb.NUMBER)
                cursor.execute(consulta_sql, {
                    "nombre"       : self.__nombre,
                    "descripcion"  : self.__descripcion,
                    "fecha_inicio" : self.__fechaInicio,
                    "fecha_termino": self.__fechaTermino,
                    "estado"       : self.__estado,
                    "id_proyecto"  : id_var,
                })
                conn.commit()
                self.__idProyecto = int(id_var.getvalue()[0])
                print(f"Proyecto '{self.__nombre}' creado con ID {self.__idProyecto}.")
                return True
            return False
        except oracledb.DatabaseError as e:
            print(f"Error al crear el proyecto: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def modificarProyecto(self, nombre: str = None, descripcion: str = None, fechaInicio: date = None, fechaTermino: date = None) -> bool:
        if nombre is not None:
            self.__nombre = nombre
        if descripcion is not None:
            self.__ = descripcion
        if fechaInicio is not None:
            self.__fechaiInicio = fechaInicio
        if fechaTermino is not None:
            self.__fechaTermino = fechaTermino

        consulta_sql = """
        UPDATE proyectos
        SET nombre = :nombre, descripcion = :descripcion,
            fecha_inicio = :fecha_inicio, fecha_termino = fecha_termino
        WHERE id_proyecto = id_proyecto
        """
        ok = self._ejecutar(consulta_sql, {
            "nombre"       : self.__nombre,
            "descripcion"  : self.__descripcion,
            "fecha_inicio" : self.__fechaInicio,
            "fecha_termino": self.__fechaTermino,
            "id_proyecto"  : self.__idProyecto,
        })
        print("Proyecto modificado correctamente" if ok else "No se pudo modificar el proyecto")
        return ok

    # Elimina el proyecto lo marca como cancelado y libera a los empleados
    def eliminarProyecto(self) -> bool:
        ok = self._ejecutar(
            "DELETE FROM proyectos WHERE id_proyecto = :id:proyecto",
            {"id_proyecto": self.__idProyecto},
        )
        print(f"Proyecto '{self.__nombre}' eliminado." if ok else "No se encontró el proyecto a eliminar.")
        return ok

    def asignarEmpleado(self, idEmpleado: int) -> bool:
        ok = self._ejecutar(
            "INSERT INTO proyecto_empleado (id_proyecto, id_empleado) "
            "VALUES (:id_proyecto, :id_empleado)",
            {"id_proyecto": self.__idProyecto, "id_empleado": idEmpleado},
        )
        print(f"Empleado {idEmpleado} asignado al proyecto." if ok
            else f"No se pudo asignar el empleado {idEmpleado}.")
        return ok

    def desasignarEmpleado(self, idEmpleado: int) -> bool:
        ok = self._ejecutar(
            "DELETE FROM proyecto_empleado "
            "WHERE id_proyecto = :id_proyecto AND id_empleado = :id_empleado",
            {"id_proyecto": self.__idProyecto, "id_empleado": idEmpleado},
        )
        print(f"Empleado {idEmpleado} liberado del proyecto." if ok
            else f"El empleado {idEmpleado} no está asignado.")
        return ok

    def cambiarEstado(self, nuevoEstado: str) -> bool:
            if nuevoEstado not in self.estados_validos:
                print(f"Estado inváldo. Use uno de: {', '.join(self.estados_validos)}")
                return False
            ok = self._ejecutar(
                "UPDATE proyectos SET estado = :estado WHERE id_proyecto = :id_proyecto",
                {"estado": nuevoEstado, "id_proyecto": self.__idProyecto},
            )
            if ok:    
                self.__estado = nuevoEstado
                print(f"Estado del proyecto cambiado a '{nuevoEstado}'.")
            return ok

    # Devuelve los proyectos guardadados en Oracle
    @staticmethod
    def listarProyectos() -> list:
        conn = None
        cursor = None
        proyectos = []
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_termino, estado
                    FROM proyectos ORDER BY id_proyecto
                """ )
                for fila in cursor.fetchall():
                    proyectos.append(Proyecto(
                        idProyecto=fila[0], nombre=fila[1], descripcion=fila[2],
                            fechaInicio=fila[3], fechaTermino=fila[4], estado=fila[5],
                    ))
        except oracledb.DatabaseError as e:
            print(f"Error al listar proyectos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return proyectos
    

    def __str__(self) -> str:
        return (f"Proyecto [{self.idProyecto}] {self.nombre} | {self.estado} | "
                f"{self.__fechaInicio} -> {self.__fechaTermino} | ")