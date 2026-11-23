from proyecto.config.app_config import conectar_db

# ARCHIVO TEMPORAL: muestra los administradores y permite borrarlos
# para volver a crear uno con la opción "2. Crear primer administrador" de main.py


def restablecer_administrador():
    conn = None
    cursor = None

    try:
        conn = conectar_db()

        if not conn:
            print("[ERROR] No se pudo conectar la bd")
            return

        cursor = conn.cursor()

        # 1. Mostrar los administradores registrados
        cursor.execute("select * from usuarios_sistema where tipo_usuario = :1", ("ADMINISTRADOR",))
        columnas = [col[0].lower() for col in cursor.description]
        administradores = cursor.fetchall()

        if not administradores:
            print("[INFO] No hay administradores. Ejecute main.py y use la opción 2.")
            return

        print("\n========== ADMINISTRADORES REGISTRADOS ==========")
        for fila in administradores:
            datos = dict(zip(columnas, fila))
            # No se muestran columnas de clave (están cifradas)
            visibles = {k: v for k, v in datos.items() if "clave" not in k and "pass" not in k}
            print(visibles)

        # 2. Confirmar antes de borrar
        confirmacion = input("\n¿Desea borrar estos administradores para crear uno nuevo? (Si | No) ").strip()

        if confirmacion != "Si":
            print("Operación cancelada. No se borró nada.")
            return

        cursor.execute("delete from usuarios_sistema where tipo_usuario = :1", ("ADMINISTRADOR",))
        conn.commit()
        print(f"[INFO] Se borraron {cursor.rowcount} administrador(es).")
        print("[INFO] Ahora ejecute main.py y elija '2. Crear primer administrador'.")

    except Exception as e:
        if conn:
            conn.rollback()  # Si algo falla, no cambia nada en la bd

        print(f"[ERROR] No se pudo completar la operación | {e}")
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    restablecer_administrador()
