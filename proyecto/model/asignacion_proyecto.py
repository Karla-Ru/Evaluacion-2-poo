from datetime import date

from proyecto.config.app_config import conectar_db, oracledb


def validar_tabla_asignacion_proyecto():
    consulta_sql = """
        create table asignaciones_proyecto (
            id_asignacion NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
            id_empleado number not null,
            id_proyecto number not null,
            fecha_asignacion date not null,
            rol_en_proyecto varchar2(50) not null,
            horas_asignadas number(5,1) not null,
            constraint uq_asignacion unique (id_empleado, id_proyecto),
            constraint ck_asignacion_horas check (horas_asignadas > 0),
            constraint fk_asignacion_empleado foreign key (id_empleado)
                references empleados(id_empleado),
            constraint fk_asignacion_proyecto foreign key (id_proyecto)
                references proyectos(id_proyecto) on delete cascade
        )
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta_sql)
            print("[INFO] Tabla asignaciones_proyecto creada correctamente")
    except oracledb.DatabaseError as e:
        error = e.args[0]

        if error.code == 955:  # la tabla ya existe
            print("[INFO] Tabla asignaciones_proyecto verificada correctamente")
        else:
            print(f"[ERROR] Creación de tabla asignaciones_proyecto | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def ejecutar_cambio_bd(consulta: str, parametros: tuple) -> bool:
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)  # Se entrega los datos parametrizados
            conn.commit()
            return cursor.rowcount > 0
        print("[ERROR] No se pudo conectar la bd")
        return False
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()  # Si algo falla aseguramos de que nada cambie en la bd

        error = e.args[0]

        if error.code == 1:
            print("[WARNING] El dato ya se encuentra registrado")
        else:
            print(f"[ERROR] Error de integridad | {e}")
        return False
    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[ERROR] Operación no realizada | {e}")
        return False
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def consultar_bd(consulta: str, parametros: tuple) -> list:
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            return cursor.fetchall()

        print("[ERROR] No se pudo conectar la bd")
        return []
    except Exception as e:
        print(f"[ERROR] Consulta no realizada | {e}")
        return []
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def obtener_id_asignacion(id_empleado: int, id_proyecto: int):
    filas = consultar_bd(
        "select id_asignacion from asignaciones_proyecto where id_empleado = :1 and id_proyecto = :2",
        (id_empleado, id_proyecto),
    )
    return int(filas[0][0]) if filas else None


def insertar_datos_asignacion(asignacion):
    consulta_insert = """
        insert into asignaciones_proyecto
            (id_empleado, id_proyecto, fecha_asignacion, rol_en_proyecto, horas_asignadas)
        values (:1, :2, :3, :4, :5)
        returning id_asignacion into :6
    """
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if conn:
            cursor = conn.cursor()
            id_generado = cursor.var(oracledb.NUMBER)  #devuelve el id creado
            cursor.execute(consulta_insert, (asignacion.id_empleado, asignacion.id_proyecto,  asignacion.fecha_asignacion, asignacion.rol_en_proyecto,
                                             asignacion.horas_asignadas, id_generado))
            conn.commit()

            asignacion.id_asignacion = int(id_generado.getvalue()[0])
            print(f"[INFO] Empleado {asignacion.id_empleado} asignado al proyecto {asignacion.id_proyecto}")
    except oracledb.IntegrityError as e:
        if conn:
            conn.rollback()

        error = e.args[0]

        if error.code == 1:  # el empleado ya estaba asignado
            print("[WARNING] El empleado ya está asignado a este proyecto")
            asignacion.id_asignacion = obtener_id_asignacion(asignacion.id_empleado, asignacion.id_proyecto)
        elif error.code == 2291:  #no existe el empleado o el proyecto
            print("[ERROR] El empleado o el proyecto no existe")
        else:
            print(f"[ERROR] Error de integridad | {e}")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Asignación no registrada | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def eliminar_asignacion_bd(id_empleado: int, id_proyecto: int) -> bool:
    eliminado = ejecutar_cambio_bd(
        "delete from asignaciones_proyecto where id_empleado = :1 and id_proyecto = :2",
        (id_empleado, id_proyecto),
    )
    if eliminado:
        print(f"[INFO] Empleado {id_empleado} desasignado del proyecto {id_proyecto}")
    else:
        print(f"[WARNING] El empleado {id_empleado} no estaba asignado al proyecto {id_proyecto}")
    return eliminado


def esta_asignado(id_empleado: int, id_proyecto: int) -> bool:
    return obtener_id_asignacion(id_empleado, id_proyecto) is not None


def listar_asignaciones_proyecto(id_proyecto: int) -> list:
    return consultar_bd("""
        select id_asignacion, id_empleado, rol_en_proyecto, horas_asignadas, fecha_asignacion
        from asignaciones_proyecto
        where id_proyecto = :1
        order by id_asignacion
    """, (id_proyecto,))


class AsignacionProyectoRepositorio():
    def __init__(self):
        pass

    def modificar_asignacion(self, rol_en_proyecto: str = None, horas_asignadas: float = None):
        """ Actualiza el rol y/o las horas asignadas en bd """
        nuevo_rol = rol_en_proyecto if rol_en_proyecto is not None else self.rol_en_proyecto
        nuevas_horas = horas_asignadas if horas_asignadas is not None else self.horas_asignadas

        if not isinstance(nuevo_rol, str) or not nuevo_rol.strip():
            print("Rol no corresponde a tipo str o está vacío")
            return False

        if not isinstance(nuevas_horas, (int, float)) or nuevas_horas <= 0:
            print("Las horas asignadas deben ser un número mayor a 0")
            return False

        actualizado = ejecutar_cambio_bd(
            "update asignaciones_proyecto set rol_en_proyecto = :1, horas_asignadas = :2 where id_asignacion = :3",
            (nuevo_rol, nuevas_horas, self.id_asignacion),
        )

        if actualizado:
            self.rol_en_proyecto = nuevo_rol
            self.horas_asignadas = nuevas_horas
            print("[INFO] Asignación actualizada correctamente")
        else:
            print("[ERROR] No se pudo actualizar la asignación")
        return actualizado

    def eliminar_asignacion(self):
        """ Elimina esta asignación de la bd """
        return eliminar_asignacion_bd(self.id_empleado, self.id_proyecto)


class AsignacionProyecto(AsignacionProyectoRepositorio):
    def __init__(self, id_empleado: int, id_proyecto: int, rol_en_proyecto: str,
                 horas_asignadas: float, fecha_asignacion: date = None):
        self.id_asignacion    = None  # Lo asigna Oracle al guardar
        self.id_empleado      = id_empleado
        self.id_proyecto      = id_proyecto
        self.fecha_asignacion = fecha_asignacion or date.today()
        self.rol_en_proyecto  = rol_en_proyecto
        self.horas_asignadas  = horas_asignadas

        self.asignar()  # Creamos la tabla, validamos que exista y guardamos

    def asignar(self):
        if not isinstance(self.rol_en_proyecto, str) or not self.rol_en_proyecto.strip():
            print("[ERROR] El rol en el proyecto no puede estar vacío")
            return False

        if not isinstance(self.horas_asignadas, (int, float)) or self.horas_asignadas <= 0:
            print("[ERROR] Las horas asignadas deben ser un número mayor a 0")
            return False

        validar_tabla_asignacion_proyecto()
        insertar_datos_asignacion(self)
        return self.id_asignacion is not None

    def mostrar_datos(self):
        return (f"Asignación de Proyecto\n ID: {self.id_asignacion} | Empleado: {self.id_empleado} | "
                f"Proyecto: {self.id_proyecto} | Rol: {self.rol_en_proyecto} | "
                f"Horas: {self.horas_asignadas} | Desde: {self.fecha_asignacion}")
