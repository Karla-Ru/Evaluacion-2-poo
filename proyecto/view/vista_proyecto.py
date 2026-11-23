from datetime import datetime, date
from proyecto.model.proyecto import (Proyecto, ProyectoRepositorio, obtener_proyecto, listar_proyectos)
from proyecto.model.asignacion_proyecto import (AsignacionProyecto, eliminar_asignacion_bd, listar_asignaciones_proyecto)
from proyecto.model.resgistro_tiempo import (RegistroTiempo, listar_registros_empleado, total_horas_proyecto, total_horas_empleado)

def pausar():
    input("\nPresione ENTER para continuar: ")

def pedir_id(texto: str):
    try:
        id_ingresado = int(input(texto))

        if id_ingresado <=0:
            print("[WARNING] El ID debe ser positivo.")
            return None
        return id_ingresado
    except ValueError:
        print("[WARNING] Ingrese un ID númerico válido.")
        return None

def pedir_fecha(texto: str):
    fecha_texto = input(texto).strip()

    try:
        return datetime.strptime(fecha_texto, "%d/%m/%Y").date()
    except ValueError:
        print("[WARNING] Formato de fecha incorrecto.")
        return None

def cargar_repositorio(id_proyecto: int):
    datos = obtener_proyecto(id_proyecto)

    if not datos:
        print("[WARNING] No existe un proyecto con ese ID.")
        return None

    repositorio               = ProyectoRepositorio()
    repositorio.id_proyecto   = datos[0]
    repositorio.nombre        = datos[1]
    repositorio.descripcion   = datos[2]
    repositorio.fecha_inicio  = datos[3].date() if isinstance(datos[3], datetime) else datos[3]
    repositorio.fecha_termino = datos[4].date() if isinstance(datos[4], datetime) else datos[4]
    repositorio.estado        = datos[5]
    return repositorio

# PROYECTOS

def registrar_proyecto():
    print("\===== REGISTRAR PROYECTO =====")

    nombre = input("Nombre del proyecto: ").strip()
    if not nombre:
        print("[WARNING] El nombre del proyecto es obligatorio.")
        return

    descripcion = input("Descripción: ").strip()

    fecha_inicio = pedir_fecha("Fecha de inicio (DD/MM/AAAA): ")
    if not fecha_inicio:
        return

    fecha_termino = pedir_fecha("Fecha de Término (DD/MM/AAAA): ")
    if not fecha_termino:
        return

    print("\Registrando proyecto...")
    Proyecto(nombre, descripcion, fecha_inicio, fecha_termino)

def mostrar_proyectos():

    print("n===== LISTADO DE PROYECTOS =====")

    proyectos = listar_proyectos() 
    if not proyectos:
        print("No hay proyectos registrados.")
        return

    for fila in proyectos:
        print(f"ID {fila[0]} | {fila[1]} | Estado: {fila[2]} | "
              f"{fila[3]:%d/%m/%Y} al {fila[4]:%d/%m/%Y}")

def modificar_proyecto():

    print("\n===== MODIFICAR PROYECTO ======")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    repositorio = cargar_repositorio(id_proyecto)
    if not repositorio:
        return

    print(f"\nProyecto actual: {repositorio.nombre}")
    print("(Deje en blanco y presione ENTER para mantener el dato actual)\n")

    nombre = input(f"Nombre [{repositorio.nombre}]: ").strip() or None
    descripcion = input(f"Descripción [{repositorio.descripcion}]: ").strip() or None

    fecha_inicio = None
    texto = input("Fecha de inicio [{repositorio.fecha_inicio:inicio:%d/%m/%Y}]:").strip()
    if texto:
        try:
            fecha_inicio = datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("[WARNING] Fomrato de fecha incorrecta.")
            return

    fecha_termino = None
    texto = input(f"Fecha de término [{repositorio.fecha_termino:%d/%m/%Y}]: ").strip()
    if texto:
        try:
            fecha_termino = datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("[WARNING] Formato de fecha incorrecto.")
            return

    repositorio.modificar_proyecto(nombre, descripcion, fecha_inicio, fecha_termino)


def cambiar_estado_proyecto():
    print("\n===== CAMBIAR ESTADO DEL PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    repositorio = cargar_repositorio(id_proyecto)
    if not repositorio:
        return

    print(f"\nEstado actual: {repositorio.estado}")
    print("\nSeleccione el nuevo estado: ")

    for numero, estado in enumerate(repositorio.estados_validos, start=1):
        print(f"{numero}. {estado}")

    opcion = input("\nSeleccione una opción: ").strip()

    if opcion in ("1", "2", "3", "4"):
        repositorio.cambiar_estado(repositorio.estados_validos[int(opcion) - 1])
    else:
        print("[WARNING] Opción no válida.")

def eliminar_proyecto():
    print("\n===== ELIMINAR PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    repositorio = cargar_repositorio(id_proyecto)
    if not repositorio:
        return

    print("\n[WARNING] También se eliminarán sus asignaciones y registros de horas.")
    confirmacion = input(f"¿Desea eliminar el proyecto '{repositorio.nombre}'? (Si | No) ").strip()

    if confirmacion == "Si":
        repositorio.eliminar_proyecto()
    else:
        print("Eliminación cancelada.")

# ASIGNACIONES

def asignar_empleado():
    print("\n===== ASIGNAR EMPLEADO A PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    if not obtener_proyecto(id_proyecto):
        print("[WARNING] No existe un proyecto con ese ID.")
        return

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    rol = input("Rol en el proyecto: ").strip()
    if not rol:
        print("[WARNING] El rol es obligatorio.")
        return

    try:
        horas = float(input("Horas asignadas: ").strip())

        if horas <= 0:
            print("[WARNING] Las horas deben ser mayores que cero.")
            return

    except ValueError:
        print("[WARNING] Ingrese un número de horas válido.")
        return

    print("\nAsignando empleado...")
    AsignacionProyecto(id_empleado, id_proyecto, rol, horas)


def desasignar_empleado():
    print("\n===== DESASIGNAR EMPLEADO PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    eliminar_asignacion_bd(id_empleado, id_proyecto)

    def ver_empleados_asignados():
        print("\n===== EMPLEADOS ASIGNADOS =====")

        id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    asignaciones = listar_asignaciones_proyecto(id_proyecto)

    if not asignaciones:
        print("El proyecto no tiene empleados asignados.")
        return

    for fila in asignaciones:
        print(f"Empleado {fila[1]} | Rol: {fila[2]} | Horas asignadas: {fila[3]} | "
              f"Desde: {fila[4]:%d/%m/%Y}")


# REGISTRO DE TIEMPO

def resgistrar_horas():
    print("\n===== REGISTRO DE TIEMPO =====")

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    try:
        horas = float(input("Horas trabajadas: ").strip())
    except ValueError:
        print("[WARNING] Ingrese un número de horas válido.")
        return

    descripcion = input("Descripción del trabajo: ").strip()

    texto = input("Fecha (DD/MM/AAAA, ENTER para hoy): ").strip()
    fecha = date.today()

    if texto:
        try:
            fecha = datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("[WARNING] Formato de fecha incorrecto.")
            return

    print("\nRegistrando horas...")
    RegistroTiempo(id_empleado, id_proyecto, horas, descripcion, fecha)

def ver_horas_empleado():
    print("\n===== HORAS DE UN EMPLEADO =====")

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    registros = listar_registros_empleado(id_empleado)

    if not registros:
        print("El empleado no tiene horas registradas.")
        return

    for fila in registros:
        print(f"{fila[2]:%d/%m/%Y} | Proyecto {fila[1]} | {fila[3]} h | {fila[4] or ''}")

    print(f"\nTotal: {total_horas_empleado(id_empleado)} horas")

def ver_horas_proyecto():
    print("\n===== TOTAL DE HORAS DE UN PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    print(f"Total de horas registradas: {total_horas_proyecto(id_proyecto)}")


# MENÚ

def menu_proyectos():

    while True:

        print("\n")
        print("============================================")
        print("          GESTIÓN DE PROYECTOS")
        print("============================================")
        print(" PROYECTOS")
        print("1. Registrar proyecto")
        print("2. Listar proyectos")
        print("3. Modificar proyecto")
        print("4. Cambiar estado del proyecto")
        print("5. Eliminar proyecto")
        print(" ASIGNACIONES")
        print("6. Asignar empleado a proyecto")
        print("7. Desasignar empleado de proyecto")
        print("8. Ver empleados asignados")
        print(" REGISTRO DE TIEMPO")
        print("9. Registrar horas trabajadas")
        print("10. Ver horas de un empleado")
        print("11. Ver total de horas de un proyecto")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_proyecto()
            pausar()

        elif opcion == "2":
            mostrar_proyectos()
            pausar()

        elif opcion == "3":
            modificar_proyecto()
            pausar()

        elif opcion == "4":
            cambiar_estado_proyecto()
            pausar()

        elif opcion == "5":
            eliminar_proyecto()
            pausar()

        elif opcion == "6":
            asignar_empleado()
            pausar()

        elif opcion == "7":
            desasignar_empleado()
            pausar()

        elif opcion == "8":
            ver_empleados_asignados()
            pausar()

        elif opcion == "9":
            registrar_horas()
            pausar()

        elif opcion == "10":
            ver_horas_empleado()
            pausar()

        elif opcion == "11":
            ver_horas_proyecto()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()