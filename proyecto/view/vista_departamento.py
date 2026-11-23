
from proyecto.model.departamento import (
    Departamento,
    DepartamentoRepositorio,
    insertar_datos_departamento
)

def pausar():
    input("\nPresione ENTER para continuar...")

def registrar_departamento():

    print("\n========== REGISTRAR DEPARTAMENTO ==========")

    nombre = input("Nombre del departamento: ").strip()

    if not nombre:
        print("[WARNING] El nombre es obligatorio.")
        return

    descripcion = input("Descripción del departamento: ").strip()

    id_gerente = input(
        "ID del empleado que será gerente (ENTER si no tiene): "
    ).strip()

    if id_gerente:
        try:
            id_gerente = int(id_gerente)

            if id_gerente <= 0:
                print("[WARNING] El ID del gerente debe ser positivo.")
                return

        except ValueError:
            print("[WARNING] Ingrese un ID numérico válido.")
            return
    else:
        id_gerente = None

    departamento = Departamento(
        nombre=nombre,
        descripcion=descripcion or None,
        id_gerente=id_gerente
    )

    insertar_datos_departamento(departamento)

def actualizar_nombre_departamento():

    print("\n========== ACTUALIZAR NOMBRE ==========")

    try:
        id_departamento = int(input("ID del departamento: "))

        if id_departamento <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return

    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return

    nuevo_nombre = input("Nuevo nombre: ").strip()

    if not nuevo_nombre:
        print("[WARNING] El nombre no puede estar vacío.")
        return

    repositorio = DepartamentoRepositorio()
    repositorio.id_departamento = id_departamento

    repositorio.actualizar_nombre(nuevo_nombre)

def actualizar_descripcion_departamento():

    print("\n========== ACTUALIZAR DESCRIPCIÓN ==========")

    try:
        id_departamento = int(input("ID del departamento: "))

        if id_departamento <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return

    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return

    nueva_descripcion = input("Nueva descripción: ").strip()

    repositorio = DepartamentoRepositorio()
    repositorio.id_departamento = id_departamento

    repositorio.actualizar_descripcion(nueva_descripcion or None)

def asignar_gerente_departamento():

    print("\n========== ASIGNAR GERENTE ==========")

    try:
        id_departamento = int(input("ID del departamento: "))
        id_gerente = int(input("ID del empleado que será gerente: "))

        if id_departamento <= 0 or id_gerente <= 0:
            print("[WARNING] Los ID deben ser positivos.")
            return

    except ValueError:
        print("[WARNING] Ingrese valores numéricos válidos.")
        return

    repositorio = DepartamentoRepositorio()
    repositorio.id_departamento = id_departamento

    repositorio.asignar_gerente(id_gerente)

def eliminar_departamento():

    print("\n========== ELIMINAR DEPARTAMENTO ==========")

    try:
        id_departamento = int(input("ID del departamento: "))

        if id_departamento <= 0:
            print("[WARNING] El ID debe ser positivo.")
            return

    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return

    confirmacion = input(
        "¿Está seguro de eliminar este departamento? (S/N): "
    ).strip().upper()

    if confirmacion != "S":
        print("Operación cancelada.")
        return

    repositorio = DepartamentoRepositorio()
    repositorio.id_departamento = id_departamento

    repositorio.eliminar_departamento()

def menu_departamentos():

    while True:

        print("\n")
        print("============================================")
        print("         GESTIÓN DE DEPARTAMENTOS")
        print("============================================")
        print("1. Registrar departamento")
        print("2. Actualizar nombre")
        print("3. Actualizar descripción")
        print("4. Asignar o cambiar gerente")
        print("5. Eliminar departamento")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_departamento()
            pausar()

        elif opcion == "2":
            actualizar_nombre_departamento()
            pausar()

        elif opcion == "3":
            actualizar_descripcion_departamento()
            pausar()

        elif opcion == "4":
            asignar_gerente_departamento()
            pausar()

        elif opcion == "5":
            eliminar_departamento()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()