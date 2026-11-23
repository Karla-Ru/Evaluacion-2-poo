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
from proyecto.model.rol import verificar_permiso

usuario_en_sesion = None #SESIÓN DEL USUARIO AUTENTICADO

def obtener_usuario_en_sesion(): #CON ESTO DESDE MAIN.PY SE PUEDE CONSULTAR AL USUARIO AUTENTICADO
    return usuario_en_sesion

def tiene_permiso(nombre_permiso: str) -> bool:

    if usuario_en_sesion is None:
        print("[WARNING] Debe iniciar sesión primero.")
        return False

    rol = usuario_en_sesion["tipo_usuario"]

    if verificar_permiso(rol, nombre_permiso):
        return True

    print("[ERROR] No tiene autorización para realizar esta operación.")
    return False

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

    if not tiene_permiso("GESTIONAR_USUARIOS"):
        return
    
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

    if not tiene_permiso("GESTIONAR_USUARIOS"):
        return

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

    global usuario_en_sesion

    if usuario_en_sesion is not None:
        print("[WARNING] Ya existe una sesión activa.")
        return

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

    if resultado is not None:
        
        usuario_en_sesion = resultado

        print("\n[INFO] Bienvenido al sistema.")
        print(f"[INFO] Usuario: {usuario_en_sesion['nombre_usuario']}")
        print(f"[INFO] Rol: {usuario_en_sesion['tipo_usuario']}")

        if usuario_en_sesion["id_empleado"] is not None:
            print(
                f"[INFO] ID de empleado: "
                f"{usuario_en_sesion['id_empleado']}"
            )

    else:
        print("\n[WARNING] No fue posible iniciar sesión.")

def cerrar_sesion():

    global usuario_en_sesion

    if usuario_en_sesion is None:
        print("[WARNING] No hay ninguna sesión activa.")
        return

    print(
        f"\n[INFO] Cerrando sesión de "
        f"{usuario_en_sesion['nombre_usuario']}..."
    )

    usuario_en_sesion = None

    print("[INFO] Sesión cerrada correctamente.")

def menu_usuarios():

    while True:

        print("\n")
        print("============================================")
        print("           GESTIÓN DE USUARIOS")
        print("============================================")
        print("1. Registrar administrador")
        print("2. Crear cuenta para empleado")
        print("-------------------------------------------")
        print("3. Iniciar sesión")
        print("4. Mostrar usuario en sesión")
        print("5. Cerrar Sesión")
        print("-------------------------------------------")
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

        elif opcion == "4":
            if usuario_en_sesion is not None:
                print("\n========== USUARIO EN SESIÓN ==========")
                print(f"ID: {usuario_en_sesion['id_usuario']}")
                print(f"Usuario: {usuario_en_sesion['nombre_usuario']}")
                print(f"Rol: {usuario_en_sesion['tipo_usuario']}")

                if usuario_en_sesion["id_empleado"] is not None:
                    print(f"Empleado asociado: {usuario_en_sesion['id_empleado']}")
            else:
                print("\n[WARNING] No hay ninguna sesión activa.")

            pausar()

        elif opcion == "5":
            cerrar_sesion()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()