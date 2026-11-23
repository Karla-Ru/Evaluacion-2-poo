from datetime import datetime
from proyecto.model.empleado import (
    Empleado,
    EmpleadoRepositorio,
    insertar_datos_empleado
)


def pausar():
    input("\nPresione ENTER para continuar...")


def registrar_empleado():

    print("\n========== REGISTRAR EMPLEADO ==========")

    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("[WARNING] El nombre es obligatorio.")
        return

    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()

    correo = input("Correo electrónico: ").strip()
    if "@" not in correo or "." not in correo:
        print("[WARNING] Ingrese un correo electrónico válido.")
        return

    fecha_texto = input("Fecha de contratación (DD/MM/AAAA): ").strip()

    try:
        fecha_contratacion = datetime.strptime(
            fecha_texto, "%d/%m/%Y"
        ).date()
    except ValueError:
        print("[WARNING] Formato de fecha incorrecto.")
        return

    try:
        salario = float(input("Salario: ").strip())

        if salario <= 0:
            print("[WARNING] El salario debe ser mayor que cero.")
            return

    except ValueError:
        print("[WARNING] Ingrese un salario numérico válido.")
        return

    empleado = Empleado(
        nombre=nombre,
        direccion=direccion,
        telefono=telefono,
        correo_electronico=correo,
        fecha_contratacion=fecha_contratacion,
        salario=salario
    )

    print("\nRegistrando empleado...")
    insertar_datos_empleado(empleado)


def actualizar_salario():

    print("\n========== ACTUALIZAR SALARIO ==========")

    try:
        id_empleado = int(input("ID del empleado: "))

        if id_empleado <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return

        nuevo_salario = float(input("Nuevo salario: "))

        if nuevo_salario <= 0:
            print("[WARNING] El salario debe ser mayor que cero.")
            return

    except ValueError:
        print("[WARNING] Ingrese valores numéricos válidos.")
        return

    repositorio = EmpleadoRepositorio()
    repositorio.id_empleado = id_empleado

    repositorio.actualizar_salario(nuevo_salario)


def cambiar_estado_empleado():

    print("\n========== CAMBIAR ESTADO DEL EMPLEADO ==========")

    try:
        id_empleado = int(input("ID del empleado: "))

        if id_empleado <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return

    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return

    print("\nSeleccione el nuevo estado:")
    print("1. Activar empleado")
    print("2. Desactivar empleado")

    opcion = input("\nSeleccione una opción: ").strip()

    if opcion == "1":
        estado = True
    elif opcion == "2":
        estado = False
    else:
        print("[WARNING] Opción no válida.")
        return

    repositorio = EmpleadoRepositorio()
    repositorio.id_empleado = id_empleado

    repositorio.cambiar_estado(estado)


def menu_empleados():

    while True:

        print("\n")
        print("============================================")
        print("          GESTIÓN DE EMPLEADOS")
        print("============================================")
        print("1. Registrar empleado")
        print("2. Actualizar salario")
        print("3. Activar / Desactivar empleado")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_empleado()
            pausar()

        elif opcion == "2":
            actualizar_salario()
            pausar()

        elif opcion == "3":
            cambiar_estado_empleado()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()
