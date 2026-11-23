from getpass import getpass

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

from proyecto.model.usuario_sistema import (
    validar_tabla_usuario_sistema,
    existe_administrador
)

from proyecto.model.administrador import (
    Administrador,
    insertar_administrador
)

from proyecto.model.rol import (
    validar_tabla_rol,
    validar_tabla_rol_permiso
)

from proyecto.model.permiso import validar_tabla_permiso


# VISTAS

from proyecto.view.vista_usuario import (
    menu_usuarios,
    iniciar_sesion,
    cerrar_sesion,
    obtener_usuario_en_sesion,
    tiene_permiso
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

from proyecto.view.vista_moneda import menu_monedas

from proyecto.view.vista_clima import menu_clima

# UTILIDADES

def pausar():
    input("\nPresione ENTER para continuar...")

# INICIALIZACIÓN DEL SISTEMA

def inicializar_sistema():

    print("\n============================================")
    print("       INICIALIZANDO ECOTECH SOLUTIONS")
    print("============================================")

    validaciones = [
        ("Empleados", validar_tabla_empleado),
        ("Departamentos", validar_tabla_departamento),
        ("Proyectos", validar_tabla_proyecto),
        ("Asignaciones", validar_tabla_asignacion_proyecto),
        ("Registros de tiempo", validar_tabla_registro_tiempo),
        ("Roles", validar_tabla_rol),
        ("Permisos", validar_tabla_permiso),
        ("Relación rol-permiso", validar_tabla_rol_permiso),
        ("Usuarios del sistema", validar_tabla_usuario_sistema)
    ]

    for nombre, funcion in validaciones:
        try:
            print(f"\n[INFO] Verificando {nombre}...")
            funcion()
        except Exception as e:
            print(f"[ERROR] No se pudo verificar {nombre}: {e}")
            raise

    print("\n[OK] Inicialización finalizada.")
    print("============================================")

# PRIMER ADMINISTRADOR

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

# GESTIÓN DE USUARIOS

def acceder_gestion_usuarios():

    menu_usuarios()

    # Si el usuario inició sesión desde el menú de usuarios,
    # recuperamos la sesión para dirigirlo a su menú correspondiente.

    usuario = obtener_usuario_en_sesion()

    if usuario is not None:
        gestionar_sesion(usuario)

# MENÚ DEL ADMINISTRADOR

def menu_administrador():

    while True:

        usuario = obtener_usuario_en_sesion()

        if usuario is None:
            print("\n[WARNING] La sesión ha finalizado.")
            return

        print("\n")
        print("============================================")
        print("          MENÚ ADMINISTRADOR")
        print("============================================")
        print("1. Gestión de empleados")
        print("2. Gestión de departamentos")
        print("3. Gestión de proyectos")
        print("4. Registro de tiempo")
        print("5. Gestión de usuarios")
        print("6. Consultar informes")
        print("7. Conversión de monedas")
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
                menu_usuarios()

        elif opcion == "6":

            if tiene_permiso("CONSULTAR_INFORMES"):
                menu_informes()

        elif opcion == "7":

            if tiene_permiso("GESTIONAR_USUARIOS"):
                menu_monedas()

        elif opcion == "0":
            cerrar_sesion()
            return

        else:
            print("\n[WARNING] Opción no válida.")

        pausar()

# MENÚ DEL EMPLEADO

def menu_empleado(usuario):

    id_empleado = usuario.get("id_empleado")

    if id_empleado is None:
        print("\n[ERROR] El usuario no tiene un empleado asociado.")
        cerrar_sesion()  # Se cierra la sesión para no quedar en un ciclo infinito
        return

    while True:

        if obtener_usuario_en_sesion() is None:
            print("\n[WARNING] La sesión ha finalizado.")
            return

        print("\n")
        print("============================================")
        print("             MENÚ EMPLEADO")
        print("============================================")
        print("1. Consultar mis datos")
        print("2. Ver mis proyectos asignados")
        print("3. Registrar mis horas")
        print("4. Consultar mis registros de tiempo")
        print("5. Consultar clima")
        print("6. Conversión de monedas")
        print("0. Cerrar sesión")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

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

                if asignaciones:
                    print("\n========== MIS PROYECTOS ==========")

                    for fila in asignaciones:
                        print(
                            f"Proyecto: {fila}"
                        )
                else:
                    print("\nNo tienes proyectos asignados.")

        elif opcion == "3":

            if tiene_permiso("REGISTRAR_HORAS"):
                registrar_mis_horas(id_empleado)

        elif opcion == "4":

            if tiene_permiso("CONSULTAR_DATOS_PROPIOS"):
                ver_mis_registros(id_empleado)

        elif opcion == "5":
            menu_clima()

        elif opcion == "6":
            menu_monedas()

        elif opcion == "0":
            cerrar_sesion()
            return

        else:
            print("\n[WARNING] Opción no válida.")

        pausar()

# CONTROL DE SESIONES

def gestionar_sesion(usuario):

    tipo_usuario = usuario.get("tipo_usuario")

    if tipo_usuario == "ADMINISTRADOR":

        menu_administrador()

    elif tipo_usuario == "EMPLEADO":

        menu_empleado(usuario)

    else:

        print("\n[ERROR] El tipo de usuario no es válido.")

        cerrar_sesion()

# MENÚ PRINCIPAL

def menu_principal():

    while True:

        usuario = obtener_usuario_en_sesion()

        if usuario is not None:
            gestionar_sesion(usuario)
            continue

        hay_administrador = existe_administrador()

        print("\n")
        print("============================================")
        print("             ECOTECH SOLUTIONS")
        print("============================================")
        print("1. Gestión de usuarios / Iniciar sesión")

        if not hay_administrador:
            print("2. Crear primer administrador")

        print("0. Salir del sistema")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            acceder_gestion_usuarios()

        elif opcion == "2" and not hay_administrador:

            crear_primer_administrador()
            pausar()

        elif opcion == "0":

            print("\n[INFO] Cerrando ECOTECH SOLUTIONS...")
            print("[INFO] Hasta pronto.")
            break

        else:

            print("\n[WARNING] Opción no válida.")
            pausar()

# EJECUCIÓN PRINCIPAL

def main():

    try:

        inicializar_sistema()

        menu_principal()

    except KeyboardInterrupt:

        print("\n\n[INFO] Ejecución interrumpida por el usuario.")

        if obtener_usuario_en_sesion() is not None:
            cerrar_sesion()

    except Exception as e:

        print(f"\n[ERROR] Error al ejecutar el sistema: {e}")

        if obtener_usuario_en_sesion() is not None:
            cerrar_sesion()


if __name__ == "__main__":
    main()
