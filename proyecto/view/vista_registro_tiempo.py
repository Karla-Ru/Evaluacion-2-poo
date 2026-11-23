from datetime import datetime, date
from proyecto.model.registro_tiempo import (
    RegistroTiempo,
    RegistroTiempoRepositorio,
    obtener_registro,
    listar_registros_empleado,
    listar_registros_proyecto,
    total_horas_empleado,
    total_horas_proyecto
)

def pausar():
    input("\nPresione ENTER para continuar...")

def pedir_id(texto: str):
    try:
        id_ingresado = int(input(texto))
        if id_ingresado <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return None
        return id_ingresado
    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return None

def pedir_horas(texto: str):
    try:
        horas = float(input(texto).strip())
        if horas <= 0 or horas > 24:
            print("[WARNING] Las horas deben ser mayores que 0 y como máximo 24")
            return None
        return horas
    except ValueError:
        print("[WARNING] Ingrese un número de horas válido")
        return None

def cargar_repositorio(id_registro: int):
    datos = obtener_registro(id_registro)

    if not datos:
        print("[WARNING] No existe un registro con ese ID.")
        return None

    repositorio                  = RegistroTiempoRepositorio()
    repositorio.id_registro      = datos[0]
    repositorio.id_empleado      = datos[1]
    repositorio.id_proyecto      = datos[2]
    repositorio.fecha            = datos[3]
    repositorio.horas_trabajadas = float(datos[4])
    repositorio.descripcion      = datos[5] or ""
    return repositorio

def registrar_horas():
    print("\n===== REGISTRAR HORAS TRABAJADAS =====")

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    horas = pedir_horas("Horas trabajadas: ")
    if not horas:
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

        if fecha > date.today():
            print("[WARNING] No se pueden registrar horas en una fecha futura.")
            return

    print("\nRegistrando horas...")
    RegistroTiempo(id_empleado, id_proyecto, horas, descripcion, fecha)

def modificar_registro():
    print("\n===== MODIFICAR REGISTRO DE HORAS =====")

    id_registro = pedir_id("ID del registro: ")
    if not id_registro:
        return

    repositorio = cargar_repositorio(id_registro)
    if not repositorio:
        return

    print(f"\nRegistro actual: {repositorio.fecha:%d/%m/%Y} | Empleado {repositorio.id_empleado} | "
          f"Proyecto {repositorio.id_proyecto} | {repositorio.horas_trabajadas} h")
    print("(Deje en blanco y presione ENTER para mantener el dato actual)\n")

    horas = None
    texto = input(f"Horas trabajadas [{repositorio.horas_trabajadas}]: ").strip()

    if texto:
        try:
            horas = float(texto)
        except ValueError:
            print("[WARNING] Ingrese un número de horas válido.")
            return

    descripcion = input(f"Descripción [{repositorio.descripcion}]: ").strip() or None

    repositorio.modificar_registro(horas, descripcion)

def eliminar_registro():
    print("\n===== ELIMINAR REGISTRO DE HORAS =====")

    id_registro = pedir_id("ID del registro: ")
    if not id_registro:
        return

    repositorio = cargar_repositorio(id_registro)
    if not repositorio:
        return

    confirmacion = input(f"¿Desea eliminar el registro de {repositorio.horas_trabajadas} h del "
                         f"{repositorio.fecha:%d/%m/%Y}? (Si | No) ").strip()

    if confirmacion == "Si":
        repositorio.eliminar_registro()
    else:
        print("Eliminación cancelada.")

def ver_registros_empleado():
    print("\n===== HORAS DE UN EMPLEADO =====")

    id_empleado = pedir_id("ID del empleado: ")
    if not id_empleado:
        return

    registros = listar_registros_empleado(id_empleado)

    if not registros:
        print("El empleado no tiene horas registradas.")
        return

    for fila in registros:
        print(f"Registro {fila[0]} | {fila[2]:%d/%m/%Y} | Proyecto {fila[1]} | "
              f"{fila[3]} h | {fila[4] or ''}")

    print(f"\nTotal: {total_horas_empleado(id_empleado)} horas")

def ver_registros_proyecto():
    print("\n===== HORAS DE UN PROYECTO =====")

    id_proyecto = pedir_id("ID del proyecto: ")
    if not id_proyecto:
        return

    registros = listar_registros_proyecto(id_proyecto)

    if not registros:
        print("El proyecto no tiene horas registradas.")
        return

    for fila in registros:
        print(f"Registro {fila[0]} | {fila[2]:%d/%m/%Y} | Empleado {fila[1]} | "
              f"{fila[3]} h | {fila[4] or ''}")

    print(f"\nTotal: {total_horas_proyecto(id_proyecto)} horas")

def menu_registro_tiempo():
    while True:

        print("\n")
        print("============================================")
        print("          REGISTRO DE TIEMPO")
        print("============================================")
        print("1. Registrar horas trabajadas")
        print("2. Modificar registro de horas")
        print("3. Eliminar registro de horas")
        print("4. Ver horas de un empleado")
        print("5. Ver horas de un proyecto")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_horas()
            pausar()

        elif opcion == "2":
            modificar_registro()
            pausar()

        elif opcion == "3":
            eliminar_registro()
            pausar()

        elif opcion == "4":
            ver_registros_empleado()
            pausar()

        elif opcion == "5":
            ver_registros_proyecto()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()
