from proyecto.model.empleado import (
    validar_tabla_empleado,
    obtener_empleado_por_id
)
from proyecto.model.departamento import validar_tabla_departamento
from proyecto.model.proyecto import validar_tabla_proyecto
from proyecto.model.asignacion_proyecto import (
    validar_tabla_asignacion_proyecto,
    listar_asignaciones_empleado
)
from proyecto.model.registro_tiempo import validar_tabla_registro_tiempo
from proyecto.model.usuario_sistema import validar_tabla_usuario_sistema
from proyecto.model.rol import (
    validar_tabla_rol,
    validar_tabla_rol_permiso
)
from proyecto.model.permiso import validar_tabla_permiso

from proyecto.view.vista_usuario import (
    iniciar_sesion,
    cerrar_sesion,
    obtener_usuario_en_sesion,
    tiene_permiso,
    registrar_administrador,
    registrar_usuario_empleado
)
from proyecto.view.vista_empleado import menu_empleados
from proyecto.view.vista_departamento import menu_departamentos
from proyecto.view.vista_proyecto import menu_proyectos
from proyecto.view.vista_registro_tiempo import (
    menu_registro_tiempo,
    registrar_mis_horas,
    ver_mis_registros
)
from proyecto.view.vista_informes import menu_informes
from proyecto.model.usuario_sistema import validar_tabla_usuario_sistema, existe_administrador
from getpass import getpass
from proyecto.model.administrador import Administrador, insertar_administrador

#INICIALIZACIÓN DEL SISTEMA

def inicializar_sistema():

    print("\n============================================")
    print("       INICIALIZANDO ECOTECH SOLUTIONS")
    print("============================================")

    validar_tabla_empleado()
    validar_tabla_departamento()
    validar_tabla_proyecto()
    validar_tabla_asignacion_proyecto()
    validar_tabla_registro_tiempo()

    validar_tabla_rol()
    validar_tabla_permiso()
    validar_tabla_rol_permiso()

    validar_tabla_usuario_sistema()

    print("\n[INFO] Inicialización del sistema finalizada.")


def crear_primer_administrador():

    # Seguridad: solo se permite si todavía no existe ningún administrador
    if existe_administrador():
        print("\n[WARNING] Ya existe un administrador. Inicie sesión con esa cuenta.")
        return

    print("\n========== CREAR PRIMER ADMINISTRADOR ==========")

    nombre_usuario = input("Nombre de usuario: ").strip()
    if not nombre_usuario:
        print("[WARNING] El nombre de usuario es obligatorio.")
        return

    clave = getpass("Contraseña (no se verá al escribir): ")
    if len(clave) < 8:
        print("[WARNING] La contraseña debe tener al menos 8 caracteres.")
        return

    confirmacion = getpass("Repita la contraseña: ")
    if clave != confirmacion:
        print("[WARNING] Las contraseñas no coinciden.")
        return

    administrador = Administrador(
        nombre_usuario=nombre_usuario,
        clave=clave
    )

    insertar_administrador(administrador)

# MENÚ INICIAL

def menu_inicial():

    while True:

        hay_administrador = existe_administrador()

        print("\n============================================")
        print("          ECOTECH SOLUTIONS")
        print("============================================")
        print("1. Iniciar sesión")

        if not hay_administrador:
            print("2. Crear primer administrador")

        print("0. Salir del sistema")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            iniciar_sesion()

            usuario = obtener_usuario_en_sesion()

            if usuario is not None:
                gestionar_sesion(usuario)

        elif opcion == "2" and not hay_administrador:

            crear_primer_administrador()

        elif opcion == "0":

            print("\n[INFO] Cerrando EcoTech Solutions...")
            break

        else:

            print("\n[WARNING] Opción no válida.")

#GESTIÓN DE USUARIOS

def menu_gestion_usuarios():

    while True:

        print("\n============================================")
        print("             GESTIÓN DE USUARIOS")
        print("============================================")
        print("1. Registrar administrador")
        print("2. Crear cuenta de empleado")
        print("0. Volver al menú administrativo")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            registrar_administrador()

        elif opcion == "2":

            registrar_usuario_empleado()

        elif opcion == "0":

            break

        else:

            print("\n[WARNING] Opción no válida.")

#MENÚ DEL ADMINISTRADOR

def menu_administrador():

    while True:

        print("\n============================================")
        print("          MENÚ DEL ADMINISTRADOR")
        print("============================================")
        print("1. Gestión de empleados")
        print("2. Gestión de departamentos")
        print("3. Gestión de proyectos")
        print("4. Registro de tiempo")
        print("5. Gestión de usuarios")
        print("6. Consultar informes")
        print("0. Cerrar sesión")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            if tiene_permiso("GESTIONAR_EMPLEADOS"):
                menu_empleados()

        elif opcion == "2":

            if tiene_permiso("GESTIONAR_DEPARTAMENTOS"):
                menu_departamentos()

        elif opcion == "3":

            if tiene_permiso("GESTIONAR_PROYECTOS"):
                menu_proyectos()

        elif opcion == "4":

            if tiene_permiso("GESTIONAR_REGISTROS_TIEMPO"):
                menu_registro_tiempo()

        elif opcion == "5":

            if tiene_permiso("GESTIONAR_USUARIOS"):
                menu_gestion_usuarios()

        elif opcion == "6":

            if tiene_permiso("CONSULTAR_INFORMES"):
                menu_informes()

        elif opcion == "0":

            print("\n[INFO] Regresando al menú inicial...")
            break

        else:

            print("\n[WARNING] Opción no válida.")

def menu_empleado(usuario):

    id_empleado = usuario.get("id_empleado")

    if id_empleado is None:
        print("[ERROR] Esta cuenta no está vinculada a un empleado.")
        return

    while True:
        print("\n========== MENÚ DEL EMPLEADO ==========")
        print("1. Consultar mis datos")
        print("2. Ver mis proyectos asignados")
        print("3. Registrar mis horas")
        print("4. Consultar mis registros de tiempo")
        print("0. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":

            if tiene_permiso("CONSULTAR_DATOS_PROPIOS"):
                empleado = obtener_empleado_por_id(id_empleado)

                if empleado:
                    print("\n" + empleado.mostrar_datos())
                else:
                    print("[WARNING] No se encontraron tus datos.")

        elif opcion == "2":

            if tiene_permiso("CONSULTAR_PROYECTOS_ASIGNADOS"):
                asignaciones = listar_asignaciones_empleado(id_empleado)

                if not asignaciones:
                    print("\nNo tienes proyectos asignados.")
                else:
                    print("\n========== MIS PROYECTOS ==========")

                    for fila in asignaciones:
                        print(
                            f"\nProyecto: {fila[2]}"
                            f"\nID: {fila[1]}"
                            f"\nDescripción: {fila[3] or 'Sin descripción'}"
                            f"\nEstado: {fila[4]}"
                            f"\nRol: {fila[5]}"
                            f"\nHoras asignadas: {fila[6]}"
                            f"\nFecha de asignación: {fila[7]}"
                        )

        elif opcion == "3":

            if tiene_permiso("REGISTRAR_HORAS"):
                registrar_mis_horas(id_empleado)

        elif opcion == "4":

            if tiene_permiso("CONSULTAR_DATOS_PROPIOS"):
                ver_mis_registros(id_empleado)

        elif opcion == "0":
            print("\nCerrando sesión...")
            break

        else:
            print("[WARNING] Opción no válida.")

#GESTIÓN DE SESIÓN

def gestionar_sesion(usuario):

    rol = usuario["tipo_usuario"]

    if rol == "ADMINISTRADOR":

        print("\n[INFO] Accediendo al menú de administrador.")

        menu_administrador()

    elif rol == "EMPLEADO":

        print("\n[INFO] Accediendo al menú de empleado.")

        menu_empleado(usuario)

    else:

        print("[ERROR] El rol del usuario no es reconocido.")

    cerrar_sesion()
#PUNTO DE ENTRADA

def main():

    inicializar_sistema()

    menu_inicial()

if __name__ == "__main__":
    main()

