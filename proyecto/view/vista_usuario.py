from getpass import getpass #PARA SOLICITAR LAS CONTRASEÑAS

from proyecto.model.administrador import (
    Administrador,
    insertar_administrador
)

from proyecto.model.usuario_empleado import (
    UsuarioEmpleado,
    insertar_usuario_empleado
)

from proyecto.model.usuario_sistema import autenticar_usuario

def pausar():
    input("\nPresione ENTER para continuar...")

def solicitar_credenciales():

    nombre_usuario = input("Nombre de usuario: ").strip()

    if not nombre_usuario:
        print("[WARNING] El nombre de usuario es obligatorio.")
        return None, None

    clave = getpass("Contraseña: ")

    if not clave:
        print("[WARNING] La contraseña no puede estar vacía.")
        return None, None

    confirmar_clave = getpass("Confirmar contraseña: ")

    if clave != confirmar_clave:
        print("[WARNING] Las contraseñas no coinciden.")
        return None, None

    return nombre_usuario, clave

def registrar_administrador():

    print("\n========== REGISTRAR ADMINISTRADOR ==========")

    nombre_usuario, clave = solicitar_credenciales()

    if nombre_usuario is None:
        return

    administrador = Administrador(
        nombre_usuario=nombre_usuario,
        clave=clave
    )

    insertar_administrador(administrador)

def registrar_usuario_empleado():

    print("\n========== CREAR CUENTA DE EMPLEADO ==========")

    nombre_usuario, clave = solicitar_credenciales()

    if nombre_usuario is None:
        return

    try:
        id_empleado = int(input("ID del empleado asociado: "))

        if id_empleado <= 0:
            print("[WARNING] El ID del empleado debe ser positivo.")
            return

    except ValueError:
        print("[WARNING] Ingrese un ID numérico válido.")
        return

    usuario = UsuarioEmpleado(
        nombre_usuario=nombre_usuario,
        clave=clave,
        id_empleado=id_empleado
    )

    insertar_usuario_empleado(usuario)

def iniciar_sesion():

    print("\n========== INICIO DE SESIÓN ==========")

    nombre_usuario = input("Nombre de usuario: ").strip()

    if not nombre_usuario:
        print("[WARNING] Ingrese su nombre de usuario.")
        return

    clave = getpass("Contraseña: ")

    if not clave:
        print("[WARNING] Ingrese su contraseña.")
        return

    resultado = autenticar_usuario(nombre_usuario, clave)

    if resultado:
        print("\n[INFO] Bienvenido al sistema.")
    else:
        print("\n[WARNING] No fue posible iniciar sesión.")

def menu_usuarios():

    while True:

        print("\n")
        print("============================================")
        print("           GESTIÓN DE USUARIOS")
        print("============================================")
        print("1. Registrar administrador")
        print("2. Crear cuenta para empleado")
        print("3. Iniciar sesión")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_administrador()
            pausar()

        elif opcion == "2":
            registrar_usuario_empleado()
            pausar()

        elif opcion == "3":
            iniciar_sesion()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()